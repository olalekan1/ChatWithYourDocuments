import uuid
from deepagents.backends import StateBackend
from langchain.tools import tool
from chatbotwithlangchain.indexing import build_vector_store


vector_store = build_vector_store()
backend = StateBackend()

@tool
def search_documents(query: str) -> str:
    """
    Searches the vector store for documents related to the query.

    Args:
        query (str): The search query.

    Returns:
        File paths of the documents that match the query saved in /retrieved/
    """
    retrieved_docs = vector_store.similarity_search(query, k=4)
    batch_id = str(uuid.uuid4())
    uploads: list[tuple[str, bytes]] = []
    saved_paths: list[str] = []

    for index, doc in enumerate(retrieved_docs, start=1):
        path = f"retrieved/{batch_id}_chunk_{index}.txt"
        content=(
            f"Source: {doc.metadata['source']}\n"
            f"Page: {doc.metadata['page']}\n"
            f"Content: {doc.page_content}\n\n"
        )
        saved_paths.append(path)
        uploads.append((path, content.encode("utf-8")))

    backend.upload_files(uploads)
    return(
        f"Retrieved and saved {len(saved_paths)} document chunks:\n" +
        "\n".join(saved_paths)
    )