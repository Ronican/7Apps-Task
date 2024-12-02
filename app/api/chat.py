from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_session
from app.models.pdf import PDF
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.pdf_indexer import PDFIndexer
from app.services.gemini_client import GeminiClient
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat/{pdf_id}", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_pdf(
    pdf_id: str,
    chat_request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    # Retrieve the PDF record from the database
    result = await session.execute(
        select(PDF).where(PDF.id == pdf_id)
    )
    pdf_record = result.scalars().first()

    if not pdf_record:
        raise HTTPException(status_code=404, detail="PDF not found.")

    # Initialize PDFIndexer
    indexer = PDFIndexer(pdf_record.extracted_text, pdf_id)

    # Get relevant text from the PDF
    try:
        relevant_text = await indexer.get_relevant_text(chat_request.message)
    except Exception as e:
        logger.error(f"Error retrieving relevant text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Generate a response using GeminiClient
    try:
        gemini_client = GeminiClient()
        ai_response = await gemini_client.generate_response(relevant_text)
    except Exception as e:
        logger.error(f"Error generating AI response: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Return the AI response to the user
    return ChatResponse(response=ai_response)
