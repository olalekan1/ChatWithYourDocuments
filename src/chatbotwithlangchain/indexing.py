import os

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv


load_dotenv()

def build_vector_store(documents: list[Document]) -> InMemoryVectorStore:
    """
    Builds an in-memory vector store from extracted documents.
    """
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        check_embedding_ctx_length=False
    )

    # Set up the text splitter with a chunk size of 1000 characters and an overlap of 200 characters
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Split the documents into chunks
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    # Create an in-memory vector store using the embeddings
    vector_store = InMemoryVectorStore(embeddings)

    # Add the chunks to the vector store
    vector_store.add_documents(documents=chunks)
    print(f"Total documents in vector store: {len(chunks)}")

    return vector_store

