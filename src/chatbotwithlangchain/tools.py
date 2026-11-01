import uuid
from deepagents.backends import StateBackend
from langchain.tools import tool
from chatbotwithlangchain.indexing import build_vector_store


vector_store = build_vector_store()
backend = StateBackend()


def retrieve_document_chunks(query: str) -> list[tuple[str, str]]:
    """Return relevant chunks with temporary paths and their original source metadata."""
    retrieved_docs = vector_store.similarity_search(query, k=8)
    batch_id = str(uuid.uuid4())
    chunks: list[tuple[str, str]] = []

    for index, doc in enumerate(retrieved_docs, start=1):
        path = f"retrieved/{batch_id}_chunk_{index}.txt"
        content=(
            f"Source: {doc.metadata['source']}\n"
            f"Page: {doc.metadata['page']}\n"
            f"Content: {doc.page_content}\n\n"
        )
        chunks.append((path, content))

    return chunks


@tool
def search_documents(query: str) -> str:
    """
    Searches the currently indexed document corpus and saves matching chunks
    for analysis within the agent.

    Args:
        query (str): The search query.

    Returns:
        Retrieved file paths and their source content.
    """
    chunks = retrieve_document_chunks(query)
    backend.upload_files(
        [(path, content.encode("utf-8")) for path, content in chunks]
    )
    return (
        f"Retrieved and saved {len(chunks)} document chunks. "
        "Each result includes its original source and page:\n\n"
        + "\n".join(
            f"Retrieved file: {path}\n{content}"
            for path, content in chunks
        )
    )