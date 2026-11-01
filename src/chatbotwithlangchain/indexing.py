import os

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from chatbotwithlangchain.file_handler import read_multiple_pdfs


load_dotenv()

def build_vector_store() -> InMemoryVectorStore:
    """
    Builds an in-memory vector store from PDF documents.
    """
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        check_embedding_ctx_length=False
    )

    # vector = embeddings.embed_query(
    #     "How do I make chicken curry?"
    # )

    # print(f"Vector dimensions: {len(vector)}")
    # print(vector[:10])

    PDF_PATHS = [
        # "pdfs/climate_change.pdf",
        # "pdfs/global_warming.pdf"
        "pdfs/AI Software Engineer - Cover Letter.pdf",
        "pdfs/AI Software Engineer - CV.pdf"
    ]
    
    # Read the PDF documents and convert them into Document objects
    documents = read_multiple_pdfs(PDF_PATHS)

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


