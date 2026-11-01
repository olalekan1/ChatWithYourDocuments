from chatbotwithlangchain.file_handler import read_multiple_pdfs


def main() -> None:
    """
    The main entry point for the chatbot application.
    """
    PDF_PATHS = [
        "pdfs/climate_change.pdf",
        "pdfs/global_warming.pdf"
    ]
        
    documents = read_multiple_pdfs(PDF_PATHS)
    print(f"Total documents read: {len(documents)}")
    print("++++++++++++++++++++++ \n\n")

    # print(documents)

    # Save the documents to a file for later use
    with open("documents.txt", "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(f"Source: {doc.metadata['source']}\n")
            f.write(f"Page: {doc.metadata['page']}\n")
            f.write(f"Content: {doc.page_content}\n\n")