from pathlib import Path
from typing import List
from langchain_core.documents import Document
from pypdf import PdfReader


def read_multiple_pdfs(file_paths: List[str|Path]) -> List[Document]:
    """
    Reads multiple PDF files and returns a list of Document objects.

    Args:
        file_paths (List[str|Path]): A list of file paths to the PDF files.

    Returns:
        List[Document]: A list of Document objects containing the text from the PDFs.
    """
    documents: List[Document] = []
    # First check if the file paths are valid
    invalid_files = [
        path for path in file_paths
        if not Path(path).is_file()
    ]

    if invalid_files:
        print(f"Invalid files: {invalid_files}")
        return documents

    for file_path in file_paths:
        path = Path(file_path)
        reader = PdfReader(path)

        pdf_metadata = reader.metadata

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(path),
                        "filename": path.name,
                        "page": page_number,
                        "total_pages": len(reader.pages),
                        "title": pdf_metadata.title if pdf_metadata else None,
                        "author": pdf_metadata.author if pdf_metadata else None,
                    }
                )
            )

    return documents
