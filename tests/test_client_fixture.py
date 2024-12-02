import pytest


@pytest.mark.asyncio
async def test_client_fixture(async_client):
    import httpx

    print(f"httpx version: {httpx.__version__}")
    print(f"Client type: {type(async_client)}")

    assert hasattr(async_client, "post"), "Client does not have a 'post' method."
    assert hasattr(async_client, "get"), "Client does not have a 'get' method."
    assert hasattr(async_client, "put"), "Client does not have a 'put' method."
