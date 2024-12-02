from pydantic import BaseModel


class PDFUploadResponse(BaseModel):
    detail: str
    pdf_id: str

    class Config:
        from_attributes = True
