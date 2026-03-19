"""Simple migration runner. Execute with: python -m src.infrastructure.database.migrate"""

import asyncio
import glob
import os
import ssl
import sys

import asyncpg

from src.infrastructure.config import settings


async def run_migrations(seed: bool = False) -> None:
    kwargs: dict = {"dsn": settings.database_url}
    if settings.app_env == "production":
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl"] = ssl_ctx

    conn = await asyncpg.connect(**kwargs)
    try:
        migrations_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "migrations")
        migrations_dir = os.path.abspath(migrations_dir)

        files = sorted(glob.glob(os.path.join(migrations_dir, "*.sql")))

        if not seed:
            files = [f for f in files if "seed" not in os.path.basename(f)]

        for filepath in files:
            filename = os.path.basename(filepath)
            print(f"Running migration: {filename}")
            with open(filepath) as f:
                sql = f.read()
            await conn.execute(sql)
            print(f"  Done: {filename}")

        print("All migrations complete.")
    finally:
        await conn.close()


if __name__ == "__main__":
    seed = "--seed" in sys.argv
    asyncio.run(run_migrations(seed=seed))
