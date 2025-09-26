import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import asyncio
from typing import Optional

async def parse_file(filename: str, file_bytes: bytes) -> str:
    lower = filename.lower()

    if lower.endswith('.pdf'):
        def _extract_pdf(b: bytes) -> str:
            text_chunks = []
            doc = fitz.open(stream=b, filetype='pdf')
            for page in doc:
                text_chunks.append(page.get_text())
            doc.close()
            return "\n".join(text_chunks)

        return await asyncio.to_thread(_extract_pdf, file_bytes)

    if lower.endswith('.html') or lower.endswith('.htm'):
        def _extract_html(b: bytes) -> str:
            soup = BeautifulSoup(b, 'html.parser')
            for script in soup(['script', 'style']):
                script.decompose()
            return soup.get_text(separator=' ', strip=True)
        return await asyncio.to_thread(_extract_html, file_bytes)

    if lower.endswith('.md') or lower.endswith('.markdown') or lower.endswith('.txt'):
        # Plain text or markdown: just decode
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_bytes.decode('latin-1')
            except Exception:
                return ''

    return ''