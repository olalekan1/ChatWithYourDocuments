import uuid

from deepagents.backends import StateBackend
from langchain.tools import tool
from langchain_core.vectorstores import VectorStore


backend = StateBackend()


def create_search_documents_tool(vector_store: VectorStore):
    """Create a search tool bound to one processed document index."""

    @tool
    def search_documents(query: str) -> str:
        """
        Search the processed document index and save matching chunks
        for analysis within the agent.

        Args:
            query: A question or focused search query about the documents.

        Returns:
            Retrieved file paths and their source content.
        """
        retrieved_docs = vector_store.similarity_search(query, k=5)
        batch_id = uuid.uuid4().hex
        uploads: list[tuple[str, bytes]] = []
        results: list[str] = []

        for index, doc in enumerate(retrieved_docs, start=1):
            path = f"retrieved/{batch_id}_chunk_{index}.txt"
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page")
            page_line = f"Page: {page}\n" if page is not None else ""
            content = (
                f"Source: {source}\n"
                f"{page_line}"
                f"Content: {doc.page_content}\n"
            )
            uploads.append((path, content.encode("utf-8")))
            results.append(f"Retrieved file: {path}\n{content}")

        if uploads:
            backend.upload_files(uploads)

        if not results:
            return "No matching document chunks were found."

        return (
            f"Retrieved and saved {len(results)} document chunks. "
            "Each result includes its original source and page when available:\n\n"
            + "\n".join(results)
        )

    return search_documents