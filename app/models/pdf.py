from sqlalchemy import Column, String, Integer, DateTime, Text
from app.models import Base  # Import the shared Base
import uuid
from datetime import datetime


class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=True)
    file_path = Column(String(512), nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    page_count = Column(Integer, nullable=True)
    extracted_text = Column(Text, nullable=True)  # Changed to Text

    def __repr__(self):
        return f"<PDF(id={self.id}, filename={self.filename})>"
