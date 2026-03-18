import re

import asyncpg

from src.domain.entities.article import Article, ArticleCategory, ArticleSearchResult
from src.domain.repositories.knowledge_repository import KnowledgeRepositoryBase


class PostgresKnowledgeRepository(KnowledgeRepositoryBase):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def search(
        self, query: str, category: ArticleCategory | None = None, limit: int = 5
    ) -> list[ArticleSearchResult]:
        sql = """
            SELECT id, title, category, content,
                   ts_rank(search_vector, plainto_tsquery('english', $1)) AS rank
            FROM knowledge_articles
            WHERE search_vector @@ plainto_tsquery('english', $1)
        """
        params: list[object] = [query]

        if category is not None:
            sql += " AND category = $2"
            params.append(category.value)

        sql += " ORDER BY rank DESC LIMIT $" + str(len(params) + 1)
        params.append(limit)

        rows = await self._pool.fetch(sql, *params)
        return [
            ArticleSearchResult(
                id=row["id"],
                title=row["title"],
                category=ArticleCategory(row["category"]),
                content=row["content"],
                rank=row["rank"],
            )
            for row in rows
        ]

    async def get_by_id(self, article_id: int) -> Article | None:
        row = await self._pool.fetchrow(
            """SELECT id, title, slug, category, content, created_by,
                      updated_at, created_at
               FROM knowledge_articles WHERE id = $1""",
            article_id,
        )
        return self._row_to_article(row) if row else None

    async def get_by_slug(self, slug: str) -> Article | None:
        row = await self._pool.fetchrow(
            """SELECT id, title, slug, category, content, created_by,
                      updated_at, created_at
               FROM knowledge_articles WHERE slug = $1""",
            slug,
        )
        return self._row_to_article(row) if row else None

    async def list_all(
        self,
        category: ArticleCategory | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Article], int]:
        where = ""
        params: list[object] = []

        if category is not None:
            where = "WHERE category = $1"
            params.append(category.value)

        count_row = await self._pool.fetchrow(
            f"SELECT COUNT(*) as total FROM knowledge_articles {where}", *params
        )
        total = count_row["total"] if count_row else 0

        offset = (page - 1) * per_page
        idx = len(params) + 1
        sql = f"""
            SELECT id, title, slug, category, content, created_by,
                   updated_at, created_at
            FROM knowledge_articles {where}
            ORDER BY updated_at DESC
            LIMIT ${idx} OFFSET ${idx + 1}
        """
        params.extend([per_page, offset])

        rows = await self._pool.fetch(sql, *params)
        articles = [self._row_to_article(row) for row in rows]
        return articles, total

    async def create(
        self,
        title: str,
        slug: str,
        category: ArticleCategory,
        content: str,
        created_by: int | None = None,
    ) -> Article:
        row = await self._pool.fetchrow(
            """INSERT INTO knowledge_articles (title, slug, category, content, created_by)
               VALUES ($1, $2, $3, $4, $5)
               RETURNING id, title, slug, category, content, created_by,
                         updated_at, created_at""",
            title,
            slug,
            category.value,
            content,
            created_by,
        )
        return self._row_to_article(row)

    async def update(
        self,
        article_id: int,
        title: str | None = None,
        category: ArticleCategory | None = None,
        content: str | None = None,
    ) -> Article | None:
        sets: list[str] = []
        params: list[object] = []
        idx = 1

        if title is not None:
            sets.append(f"title = ${idx}")
            params.append(title)
            idx += 1
        if category is not None:
            sets.append(f"category = ${idx}")
            params.append(category.value)
            idx += 1
        if content is not None:
            sets.append(f"content = ${idx}")
            params.append(content)
            idx += 1

        if not sets:
            return await self.get_by_id(article_id)

        sets.append("updated_at = NOW()")
        params.append(article_id)

        sql = f"""
            UPDATE knowledge_articles SET {', '.join(sets)}
            WHERE id = ${idx}
            RETURNING id, title, slug, category, content, created_by,
                      updated_at, created_at
        """
        row = await self._pool.fetchrow(sql, *params)
        return self._row_to_article(row) if row else None

    async def delete(self, article_id: int) -> bool:
        result = await self._pool.execute(
            "DELETE FROM knowledge_articles WHERE id = $1", article_id
        )
        return result == "DELETE 1"

    async def list_categories(self) -> list[str]:
        rows = await self._pool.fetch(
            "SELECT DISTINCT category FROM knowledge_articles ORDER BY category"
        )
        return [row["category"] for row in rows]

    @staticmethod
    def generate_slug(title: str) -> str:
        slug = title.lower().strip()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug.strip("-")

    @staticmethod
    def _row_to_article(row: asyncpg.Record) -> Article:
        return Article(
            id=row["id"],
            title=row["title"],
            slug=row["slug"],
            category=ArticleCategory(row["category"]),
            content=row["content"],
            created_by=row["created_by"],
            updated_at=row["updated_at"],
            created_at=row["created_at"],
        )
