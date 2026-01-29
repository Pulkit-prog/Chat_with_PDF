"""
PDF document loading and processing.
"""
from pathlib import Path
from typing import Optional
from config import Config


class PDFLoader:
    """Load and extract text from PDF files."""

    def __init__(self):
        self.supported_formats = {".pdf"}

    def load_pdf(self, filepath: str) -> tuple[Optional[str], Optional[str]]:
        """
        Load text from PDF file.

        Returns:
            Tuple of (text, filename) or (None, None) if failed
        """
        path = Path(filepath)

        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return None, None

        if path.suffix.lower() not in self.supported_formats:
            print(f"❌ Unsupported file format: {path.suffix}")
            return None, None

        try:
            text = self._extract_text(path)
            if not text or not text.strip():
                print(f"⚠️ PDF is empty: {path.name}")
                return None, None
            return text, path.name
        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            return None, None

    def _extract_text(self, filepath: Path) -> str:
        # Attempt 1: PyPDF2
        try:
            import PyPDF2
            text = []
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            combined = "\n".join(text).strip()
            if combined:
                return combined
        except Exception:
            pass

        # Attempt 2: pdfplumber (fallback)
        try:
            import pdfplumber
            text = []
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            combined = "\n".join(text).strip()
            if combined:
                return combined
            return ""
        except Exception as e:
            raise Exception(f"PDF extraction failed: {e}")
