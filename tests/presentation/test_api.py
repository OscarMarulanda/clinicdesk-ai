"""Integration tests for REST API endpoints."""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest_asyncio.fixture(scope="session")
async def client(pool):  # depends on pool to ensure app.state is set up
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
async def admin_token(client):
    res = await client.post("/api/auth/login", json={
        "email": "admin@clinicdesk.com", "password": "demo123",
    })
    assert res.status_code == 200
    return res.json()["token"]


@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


class TestHealth:
    @pytest.mark.asyncio
    async def test_health(self, client):
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json() == {"status": "ok"}


class TestAuth:
    @pytest.mark.asyncio
    async def test_login_success(self, client):
        res = await client.post("/api/auth/login", json={
            "email": "admin@clinicdesk.com", "password": "demo123",
        })
        assert res.status_code == 200
        data = res.json()
        assert "token" in data
        assert data["user"]["role"] == "admin"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client):
        res = await client.post("/api/auth/login", json={
            "email": "admin@clinicdesk.com", "password": "wrong",
        })
        assert res.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        res = await client.post("/api/auth/login", json={
            "email": "nobody@example.com", "password": "test",
        })
        assert res.status_code == 401


class TestArticlesAPI:
    @pytest.mark.asyncio
    async def test_list_articles(self, client, admin_headers):
        res = await client.get("/api/admin/articles", headers=admin_headers)
        assert res.status_code == 200
        assert res.json()["total"] >= 67

    @pytest.mark.asyncio
    async def test_list_with_category(self, client, admin_headers):
        res = await client.get("/api/admin/articles?category=scheduling", headers=admin_headers)
        assert res.status_code == 200
        for a in res.json()["articles"]:
            assert a["category"] == "scheduling"

    @pytest.mark.asyncio
    async def test_crud_article(self, client, admin_headers):
        # Create
        res = await client.post("/api/admin/articles", headers=admin_headers, json={
            "title": "Test API Article", "category": "scheduling", "content": "Test content",
        })
        assert res.status_code == 201
        aid = res.json()["id"]

        # Get
        res = await client.get(f"/api/admin/articles/{aid}", headers=admin_headers)
        assert res.status_code == 200
        assert res.json()["title"] == "Test API Article"

        # Update
        res = await client.put(f"/api/admin/articles/{aid}", headers=admin_headers, json={"title": "Updated"})
        assert res.status_code == 200
        assert res.json()["title"] == "Updated"

        # Delete
        res = await client.delete(f"/api/admin/articles/{aid}", headers=admin_headers)
        assert res.status_code == 204

        # Verify gone
        res = await client.get(f"/api/admin/articles/{aid}", headers=admin_headers)
        assert res.status_code == 404

    @pytest.mark.asyncio
    async def test_requires_auth(self, client):
        res = await client.get("/api/admin/articles")
        assert res.status_code == 401  # no auth header → Unauthorized

    @pytest.mark.asyncio
    async def test_requires_admin(self, client):
        login = await client.post("/api/auth/login", json={
            "email": "maria@brightsmile.com", "password": "demo123",
        })
        token = login.json()["token"]
        res = await client.get("/api/admin/articles", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 403


class TestSessionsAPI:
    @pytest.mark.asyncio
    async def test_list_sessions(self, client, admin_headers):
        res = await client.get("/api/admin/sessions", headers=admin_headers)
        assert res.status_code == 200
        assert "sessions" in res.json()

    @pytest.mark.asyncio
    async def test_nonexistent_session(self, client, admin_headers):
        res = await client.get("/api/admin/sessions/00000000-0000-0000-0000-000000000000", headers=admin_headers)
        assert res.status_code == 404


class TestEscalationsAPI:
    @pytest.mark.asyncio
    async def test_list_escalations(self, client, admin_headers):
        res = await client.get("/api/admin/escalations", headers=admin_headers)
        assert res.status_code == 200
        assert "escalations" in res.json()


class TestAnalyticsAPI:
    @pytest.mark.asyncio
    async def test_get_analytics(self, client, admin_headers):
        res = await client.get("/api/admin/analytics", headers=admin_headers)
        assert res.status_code == 200
        data = res.json()
        assert "total_sessions" in data
        assert "escalation_rate" in data

    @pytest.mark.asyncio
    async def test_analytics_period(self, client, admin_headers):
        res = await client.get("/api/admin/analytics?days=7", headers=admin_headers)
        assert res.json()["period_days"] == 7


class TestPublicMessages:
    @pytest.mark.asyncio
    async def test_nonexistent_session(self, client):
        res = await client.get("/api/sessions/00000000-0000-0000-0000-000000000000/messages")
        assert res.status_code == 404
