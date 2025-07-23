# ==============================================================================
# File: context_retrieval.py
# Component: 4. Context Retrieval Engine
# ==============================================================================
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
# New (recommended)
from langchain_chroma import Chroma


import config

def retrieve_context(query: str, n_results: int = 3) -> str:
    """
    Retrieves relevant context from the knowledge base for a given query.
    """
    print(f"--- Retrieving context for query: '{query}' ---")
    
    # Initialize the embedding function
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load the persisted vector store
    vector_store = Chroma(
        persist_directory=config.CHROMA_PERSIST_DIR,
        embedding_function=embedding_function,
        collection_name=config.CHROMA_COLLECTION_NAME
    )

    # Perform similarity search
    results = vector_store.similarity_search(query, k=n_results)

    if not results:
        print("No relevant context found.")
        return ""

    # Format the retrieved context
    context = "\n\n---\n\n".join([doc.page_content for doc in results])
    print("--- Context retrieval complete ---")
    return context
