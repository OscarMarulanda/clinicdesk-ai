import ssl

import asyncpg

from src.infrastructure.config import settings

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        kwargs: dict = {
            "dsn": settings.database_url,
            "min_size": 2,
            "max_size": 10,
        }
        # Enable SSL for production (required by Supabase)
        if settings.app_env == "production":
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
            kwargs["ssl"] = ssl_ctx
            # Supabase pooler doesn't support prepared statements
            kwargs["statement_cache_size"] = 0

        _pool = await asyncpg.create_pool(**kwargs)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
