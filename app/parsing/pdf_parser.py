from pathlib import Path

import pymupdf

from app.parsing.models import Page


def extract_pages(pdf_path: str | Path) -> list[Page]:
    """Extract text from a PDF while preserving page numbers."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append(
                Page(
                    page_number=page_number,
                    text=text,
                )
            )

    return pages