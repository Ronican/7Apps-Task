import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_upload_invalid_file_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open("tests/sample_files/invalid.txt", "rb") as f:
            response = await ac.post(
                "/v1/pdf", files={"file": ("invalid.txt", f, "text/plain")}
            )
    print("Response JSON:", response.json())  # Debugging statement
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."


@pytest.mark.asyncio
async def test_upload_large_pdf():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create a dummy large PDF file (e.g., 51MB)
        large_content = b"%PDF-1.4\n" + b"0" * (51 * 1024 * 1024)
        response = await ac.post(
            "/v1/pdf", files={"file": ("large.pdf", large_content, "application/pdf")}
        )
    print("Response JSON:", response.json())  # Debugging statement
    assert response.status_code == 400
    assert response.json()["detail"] == "File size exceeds the 50MB limit."


@pytest.mark.asyncio
async def test_upload_valid_pdf(async_client):
    with open("tests/sample_files/valid.pdf", "rb") as f:
        response = await async_client.post(
            "/v1/pdf", files={"file": ("valid.pdf", f, "application/pdf")}
        )
    print("Response JSON:", response.json())  # Debugging statement
    # Assert status code
    assert response.status_code == 201

    # Assert response content
    response_json = response.json()
    assert response_json["detail"] == "PDF uploaded successfully."
    assert "pdf_id" in response_json
    assert isinstance(response_json["pdf_id"], str)
