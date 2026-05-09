"""
Management command to migrate data from SQLite to PostgreSQL.

Usage:
    python manage.py migrate_sqlite_to_postgres
    python manage.py migrate_sqlite_to_postgres --sqlite-path /custom/path/db.sqlite3
    python manage.py migrate_sqlite_to_postgres --dry-run

The command reads all rows from the SQLite database and inserts them into
the default (PostgreSQL) database, preserving primary keys and all foreign
key relationships. Models are migrated in dependency order:

    Category → Supplier → Equipment → StockMovement

Existing rows in PostgreSQL are skipped (insert-or-skip semantics), so the
command is safe to run more than once.
"""

import sqlite3
from datetime import datetime, timezone

from django.core.management.base import BaseCommand, CommandError
from django.db import connections, transaction

from inventory.models import Category, Equipment, StockMovement, Supplier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_dt(value):
    """
    Parse a datetime string stored by SQLite into an aware datetime object.

    SQLite stores datetimes as ISO-8601 strings, e.g.:
        '2024-01-15 10:30:00'
        '2024-01-15 10:30:00.123456'
        '2024-01-15T10:30:00+00:00'

    Django's USE_TZ=True requires timezone-aware datetimes when writing to
    PostgreSQL, so we always attach UTC if no timezone info is present.
    """
    if value is None:
        return None

    # SQLite sometimes stores with a space separator; normalise to 'T'.
    value = value.replace(' ', 'T')

    for fmt in (
        '%Y-%m-%dT%H:%M:%S.%f%z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
    ):
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    raise ValueError(f"Cannot parse datetime string: {value!r}")


def _parse_date(value):
    """Parse a date string (YYYY-MM-DD) stored by SQLite."""
    if value is None:
        return None
    from datetime import date
    return date.fromisoformat(value)


# ---------------------------------------------------------------------------
# Per-model migration helpers
# ---------------------------------------------------------------------------

def _migrate_categories(cursor, dry_run, stdout, style):
    """Migrate inventory_category rows."""
    cursor.execute(
        "SELECT id, name, description, created_at, updated_at "
        "FROM inventory_category ORDER BY id"
    )
    rows = cursor.fetchall()

    created = skipped = 0
    for row in rows:
        pk, name, description, created_at, updated_at = row
        if dry_run:
            stdout.write(f"  [dry-run] Category id={pk} name={name!r}")
            created += 1
            continue

        obj, was_created = Category.objects.using('default').get_or_create(
            pk=pk,
            defaults={
                'name': name,
                'description': description or '',
            },
        )
        if was_created:
            # Overwrite auto_now_add / auto_now timestamps with the original values.
            Category.objects.using('default').filter(pk=pk).update(
                created_at=_parse_dt(created_at),
                updated_at=_parse_dt(updated_at),
            )
            created += 1
        else:
            skipped += 1

    return created, skipped


def _migrate_suppliers(cursor, dry_run, stdout, style):
    """Migrate inventory_supplier rows."""
    cursor.execute(
        "SELECT id, name, contact_person, email, phone, address, "
        "       created_at, updated_at "
        "FROM inventory_supplier ORDER BY id"
    )
    rows = cursor.fetchall()

    created = skipped = 0
    for row in rows:
        pk, name, contact_person, email, phone, address, created_at, updated_at = row
        if dry_run:
            stdout.write(f"  [dry-run] Supplier id={pk} name={name!r}")
            created += 1
            continue

        obj, was_created = Supplier.objects.using('default').get_or_create(
            pk=pk,
            defaults={
                'name': name,
                'contact_person': contact_person or '',
                'email': email or '',
                'phone': phone or '',
                'address': address or '',
            },
        )
        if was_created:
            Supplier.objects.using('default').filter(pk=pk).update(
                created_at=_parse_dt(created_at),
                updated_at=_parse_dt(updated_at),
            )
            created += 1
        else:
            skipped += 1

    return created, skipped


def _migrate_equipment(cursor, dry_run, stdout, style):
    """Migrate inventory_equipment rows."""
    cursor.execute(
        "SELECT id, name, category_id, equipment_type, model_number, "
        "       serial_number, description, supplier_id, purchase_price, "
        "       selling_price, quantity_in_stock, minimum_stock_level, "
        "       expiry_date, location, image, is_active, created_at, updated_at "
        "FROM inventory_equipment ORDER BY id"
    )
    rows = cursor.fetchall()

    created = skipped = 0
    for row in rows:
        (pk, name, category_id, equipment_type, model_number, serial_number,
         description, supplier_id, purchase_price, selling_price,
         quantity_in_stock, minimum_stock_level, expiry_date, location,
         image, is_active, created_at, updated_at) = row

        if dry_run:
            stdout.write(f"  [dry-run] Equipment id={pk} serial={serial_number!r}")
            created += 1
            continue

        obj, was_created = Equipment.objects.using('default').get_or_create(
            pk=pk,
            defaults={
                'name': name,
                'category_id': category_id,
                'equipment_type': equipment_type,
                'model_number': model_number or '',
                'serial_number': serial_number,
                'description': description or '',
                'supplier_id': supplier_id,
                'purchase_price': purchase_price,
                'selling_price': selling_price,
                'quantity_in_stock': quantity_in_stock,
                'minimum_stock_level': minimum_stock_level,
                'expiry_date': _parse_date(expiry_date),
                'location': location or '',
                'image': image or '',
                'is_active': bool(is_active),
            },
        )
        if was_created:
            Equipment.objects.using('default').filter(pk=pk).update(
                created_at=_parse_dt(created_at),
                updated_at=_parse_dt(updated_at),
            )
            created += 1
        else:
            skipped += 1

    return created, skipped


def _migrate_stock_movements(cursor, dry_run, stdout, style):
    """Migrate inventory_stockmovement rows."""
    cursor.execute(
        "SELECT id, equipment_id, movement_type, quantity, reason, "
        "       reference_number, performed_by_id, created_at "
        "FROM inventory_stockmovement ORDER BY id"
    )
    rows = cursor.fetchall()

    created = skipped = 0
    for row in rows:
        (pk, equipment_id, movement_type, quantity, reason,
         reference_number, performed_by_id, created_at) = row

        if dry_run:
            stdout.write(
                f"  [dry-run] StockMovement id={pk} "
                f"equipment_id={equipment_id} type={movement_type!r}"
            )
            created += 1
            continue

        obj, was_created = StockMovement.objects.using('default').get_or_create(
            pk=pk,
            defaults={
                'equipment_id': equipment_id,
                'movement_type': movement_type,
                'quantity': quantity,
                'reason': reason or '',
                'reference_number': reference_number or '',
                'performed_by_id': performed_by_id,
            },
        )
        if was_created:
            StockMovement.objects.using('default').filter(pk=pk).update(
                created_at=_parse_dt(created_at),
            )
            created += 1
        else:
            skipped += 1

    return created, skipped


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = (
        'Migrate inventory data (Category, Supplier, Equipment, StockMovement) '
        'from a SQLite database file into the default PostgreSQL database. '
        'Existing rows are skipped, so the command is safe to run repeatedly.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--sqlite-path',
            default='/app/data/db.sqlite3',
            help=(
                'Absolute path to the SQLite database file. '
                'Defaults to /app/data/db.sqlite3 (Railway persistent volume).'
            ),
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help='Print what would be migrated without writing anything to PostgreSQL.',
        )

    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        sqlite_path = options['sqlite_path']
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY-RUN mode — no data will be written.')
            )

        # ── 1. Open the SQLite file ────────────────────────────────────────
        self.stdout.write(f'\nConnecting to SQLite database at: {sqlite_path}')
        try:
            conn = sqlite3.connect(sqlite_path)
        except sqlite3.OperationalError as exc:
            raise CommandError(
                f'Cannot open SQLite database at {sqlite_path!r}: {exc}'
            ) from exc

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verify the expected tables exist.
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'inventory_%'"
        )
        found_tables = {row[0] for row in cursor.fetchall()}
        required_tables = {
            'inventory_category',
            'inventory_supplier',
            'inventory_equipment',
            'inventory_stockmovement',
        }
        missing = required_tables - found_tables
        if missing:
            conn.close()
            raise CommandError(
                f'The following expected tables are missing from the SQLite '
                f'database: {", ".join(sorted(missing))}. '
                f'Make sure you are pointing at the correct file.'
            )

        # ── 2. Migrate each model in dependency order ──────────────────────
        steps = [
            ('Category',      _migrate_categories),
            ('Supplier',      _migrate_suppliers),
            ('Equipment',     _migrate_equipment),
            ('StockMovement', _migrate_stock_movements),
        ]

        totals = {}
        try:
            with transaction.atomic(using='default'):
                for label, migrate_fn in steps:
                    self.stdout.write(f'\nMigrating {label}…')
                    created, skipped = migrate_fn(
                        cursor, dry_run, self.stdout, self.style
                    )
                    totals[label] = (created, skipped)
                    self.stdout.write(
                        f'  → {created} created, {skipped} skipped'
                    )

                if dry_run:
                    # Roll back the transaction so nothing is persisted.
                    transaction.set_rollback(True, using='default')
        finally:
            conn.close()

        # ── 3. Reset PostgreSQL sequences so future inserts don't collide ──
        if not dry_run:
            self._reset_sequences()

        # ── 4. Summary ────────────────────────────────────────────────────
        self.stdout.write('\n' + '─' * 50)
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY-RUN complete — nothing was written.'))
        else:
            self.stdout.write(self.style.SUCCESS('Migration complete!'))

        self.stdout.write('\nSummary:')
        total_created = total_skipped = 0
        for label, (created, skipped) in totals.items():
            self.stdout.write(f'  {label:<20} {created:>5} created  {skipped:>5} skipped')
            total_created += created
            total_skipped += skipped
        self.stdout.write('─' * 50)
        self.stdout.write(
            f'  {"TOTAL":<20} {total_created:>5} created  {total_skipped:>5} skipped'
        )

    # ------------------------------------------------------------------

    def _reset_sequences(self):
        """
        Reset PostgreSQL auto-increment sequences for all four models so that
        the next INSERT gets an id higher than the maximum already present.

        This is only needed for PostgreSQL; the method is a no-op for other
        backends (e.g. SQLite in tests).
        """
        default_conn = connections['default']
        if 'postgresql' not in default_conn.vendor:
            return

        self.stdout.write('\nResetting PostgreSQL sequences…')
        models = [Category, Supplier, Equipment, StockMovement]
        with default_conn.cursor() as pg_cursor:
            for model in models:
                table = model._meta.db_table
                pg_cursor.execute(
                    f"SELECT setval("
                    f"  pg_get_serial_sequence('{table}', 'id'), "
                    f"  COALESCE((SELECT MAX(id) FROM \"{table}\"), 1)"
                    f")"
                )
        self.stdout.write('  → Sequences reset successfully.')
