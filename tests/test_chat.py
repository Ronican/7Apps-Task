import pytest
from httpx import AsyncClient
from app.main import app
from app.models.pdf import PDF
from unittest.mock import patch, MagicMock, AsyncMock
from app.core.database import get_session

@pytest.mark.asyncio
async def test_chat_with_pdf(async_client: AsyncClient):
    # Mock PDF record
    pdf_id = "test_pdf_id"
    pdf_record = PDF(
        id=pdf_id,
        filename="valid.pdf",
        file_path="tests/sample_files/valid.pdf",
        page_count=10,
        extracted_text="This is a test PDF content."
    )

    # Mock database session
    class MockAsyncSession:
        async def execute(self, stmt):
            mock_result = MagicMock()
            mock_scalars = MagicMock()
            mock_scalars.first.return_value = pdf_record
            mock_result.scalars.return_value = mock_scalars
            return mock_result

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    # Override the get_session dependency
    async def override_get_session():
        yield MockAsyncSession()

    # Use try-finally to ensure cleanup
    try:
        app.dependency_overrides[get_session] = override_get_session

        # Mock GeminiClient
        with patch("app.api.chat.GeminiClient") as MockGeminiClient:
            mock_gemini_instance = MockGeminiClient.return_value
            mock_gemini_instance.generate_response = AsyncMock(return_value="This is a response from Gemini.")

            # Mock PDFIndexer.get_relevant_text
            with patch("app.api.chat.PDFIndexer.get_relevant_text", new_callable=AsyncMock) as mock_get_relevant_text:
                mock_get_relevant_text.return_value = "Relevant content from the PDF."

                # Send POST request to chat endpoint
                response = await async_client.post(
                    f"/v1/chat/{pdf_id}",
                    json={"message": "What is the content of the PDF?"}
                )

                # Assert response
                assert response.status_code == 200
                response_json = response.json()
                assert "response" in response_json
                assert response_json["response"] == "This is a response from Gemini."
    finally:
        # Clean up the dependency override
        app.dependency_overrides = {}
