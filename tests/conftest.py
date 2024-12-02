import pytest_asyncio
from app.main import app  
from httpx import AsyncClient, ASGITransport
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from app.core.database import engine, Base


@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    # Before each test
    app.dependency_overrides = {}
    yield
    # After each test
    app.dependency_overrides = {}
    
@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)