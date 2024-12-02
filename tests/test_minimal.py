import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
def read_test():
    return {"message": "Test Successful"}


@pytest.mark.asyncio
async def test_read_test():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Test Successful"}
