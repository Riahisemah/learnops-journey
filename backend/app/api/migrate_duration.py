"""
=============================================================
 MIGRATION: lessons.duration  String → Integer
=============================================================
 Run ONCE if you already have data in the DB with "MM:SS"
 duration strings. Safe to skip if you're starting fresh
 (seed_db.py already writes integers).

 Usage:
   docker cp migrate_duration.py didacticiel_api:/app/migrate_duration.py
   docker exec didacticiel_api python migrate_duration.py
=============================================================
"""

from app.database import SessionLocal, engine
from sqlalchemy import text


def migrate():
    db = SessionLocal()
    try:
        # 1. Add a temporary integer column
        with engine.connect() as conn:
            # Check if column is already integer type (idempotent guard)
            result = conn.execute(text(
                "SELECT data_type FROM information_schema.columns "
                "WHERE table_name='lessons' AND column_name='duration'"
            )).fetchone()

            if result and result[0] in ("integer", "bigint"):
                print("✅ duration column is already INTEGER — nothing to do.")
                return

            print("🔄 Converting lessons.duration from VARCHAR to INTEGER...")

            # Add temp column
            conn.execute(text("ALTER TABLE lessons ADD COLUMN duration_int INTEGER"))

            # Parse "MM:SS" → total minutes (or plain numbers)
            conn.execute(text("""
                UPDATE lessons
                SET duration_int = CASE
                    WHEN duration ~ '^[0-9]+:[0-9]+$'
                    THEN CAST(split_part(duration, ':', 1) AS INTEGER)
                    WHEN duration ~ '^[0-9]+$'
                    THEN CAST(duration AS INTEGER)
                    ELSE 0
                END
            """))

            # Drop old column and rename new one
            conn.execute(text("ALTER TABLE lessons DROP COLUMN duration"))
            conn.execute(text("ALTER TABLE lessons RENAME COLUMN duration_int TO duration"))

            conn.commit()

        print("✅ Migration complete — lessons.duration is now INTEGER (minutes).")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()