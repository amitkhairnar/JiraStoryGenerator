# ==============================================================================
# File: knowledge_base_manager.py
# Component: 3. Knowledge Base (Vector Database) - Setup Script
# ==============================================================================
import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
# from langchain_community.document_loaders import ConfluenceLoader # Commented out
import config

def load_documents_from_directory(directory_path):
    """Loads all .txt files from a directory."""
    documents_content = []
    print(f"--- Loading documents from local directory: {directory_path} ---")
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                documents_content.append(f.read())
    return documents_content

def main():
    """
    Main function to create and populate the vector database from local mock data.
    """
    print("--- Starting Knowledge Base Setup ---")

    # 1. Load documents from the local mock_data directory
    documents = load_documents_from_directory("mock_data")
    if not documents:
        print("No documents found in /mock_data. Aborting setup.")
        return

    print(f"Loaded {len(documents)} documents from local directory.")

    # 2. Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.create_documents(documents)
    print(f"Split documents into {len(docs)} chunks.")

    # 3. Initialize embedding model
    print("Initializing embedding model (this may take a moment)...")
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Create ChromaDB vector store and persist it
    print(f"Creating vector store in '{config.CHROMA_PERSIST_DIR}'...")
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=config.CHROMA_PERSIST_DIR,
        collection_name=config.CHROMA_COLLECTION_NAME
    )
    
    # Persist the database to disk
    vector_store.persist()

    print("--- Knowledge Base Setup Complete! ---")
    print(f"Vector store created and persisted in '{config.CHROMA_PERSIST_DIR}'.")

if __name__ == "__main__":
    main()
