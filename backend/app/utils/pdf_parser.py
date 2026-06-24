"""Utility functions for parsing PDF resumes using pdfplumber with PyMuPDF as fallback."""
import io
import re
import pdfplumber
import fitz  # PyMuPDF

def clean_text(text: str) -> str:
    """Normalize whitespace and remove non-printable characters."""
    if not text:
        return ""
    # Replace multiple spaces/newlines with single space/newline
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    # Remove control characters
    text = "".join(c for c in text if c.isprintable() or c in ['\n', '\r', '\t'])
    return text.strip()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes. Tries pdfplumber first, falls back to fitz."""
    extracted_text = ""
    
    # Try pdfplumber
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text_list = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_list.append(page_text)
            extracted_text = "\n\n".join(text_list)
    except Exception as e:
        # Fallback to PyMuPDF (fitz)
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text_list = []
            for page in doc:
                text_list.append(page.get_text("text", sort=True))
            extracted_text = "\n\n".join(text_list)
            doc.close()
        except Exception as fallback_e:
            raise ValueError(f"Failed to parse PDF resume: {fallback_e}") from e
            
    cleaned = clean_text(extracted_text)
    if len(cleaned) < 50:
        raise ValueError("The uploaded PDF does not contain enough extractable text. Please make sure it is a text-based PDF and not a scanned document/image.")
    return cleaned
