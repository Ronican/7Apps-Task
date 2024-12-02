from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.pdf import PDF
from app.services.pdf_processor import process_pdf
from app.schemas.pdf import PDFUploadResponse
from uuid import uuid4
import os

router = APIRouter()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@router.post(
    "/pdf", response_model=PDFUploadResponse, status_code=status.HTTP_201_CREATED
)
async def upload_pdf(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    # 1. Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are allowed."
        )

    # 2. Read file content to check size
    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read uploaded file.")

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 50MB limit.")

    # 3. Generate unique filename and save the file
    unique_id = str(uuid4())
    filename = f"{unique_id}_{file.filename}"
    file_path = os.path.join("app/uploads", filename)

    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    # 4. Process the PDF
    try:
        page_count, extracted_text = await process_pdf(file_path)
    except Exception:
        # Cleanup the saved file if processing fails
        os.remove(file_path)
        raise HTTPException(
            status_code=400, detail="Uploaded PDF is corrupted or invalid."
        )

    # 5. Create and commit the PDF record
    pdf_record = PDF(
        id=unique_id,
        filename=file.filename,
        file_path=file_path,
        page_count=page_count,
        extracted_text=extracted_text,
    )

    session.add(pdf_record)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        # Cleanup the saved file if database commit fails
        os.remove(file_path)
        raise HTTPException(status_code=500, detail="Database commit failed.")

    # 6. Return the successful response
    response = PDFUploadResponse(detail="PDF uploaded successfully.", pdf_id=unique_id)
    print("Returning response:", response.dict())  # Debugging statement
    return response
