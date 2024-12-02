import os
from pypdf import PdfReader
import uuid
from typing import Tuple


UPLOAD_DIR = "app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename to prevent directory traversal attacks and collisions.
    """
    # Extract the base name to prevent directory traversal
    base_name = os.path.basename(filename)
    # Generate a unique filename using UUID
    unique_name = f"{uuid.uuid4()}_{base_name}"
    return unique_name


async def process_pdf(file_path: str) -> Tuple[int, str]:
    try:
        reader = PdfReader(file_path)
        page_count = len(reader.pages)
        extracted_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return page_count, extracted_text
    except Exception as e:
        # Log the exception if necessary
        raise e
