import os
import shutil
import git
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_community.document_loaders import GitLoader, DirectoryLoader, TextLoader
import config

# ----------------------
# Logging Setup
# ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ----------------------
# Helper Functions
# ----------------------

def get_default_branch(repo):
    """Attempts to identify the default branch of a Git repo."""
    try:
        return repo.git.symbolic_ref("refs/remotes/origin/HEAD").split("/")[-1]
    except Exception as e:
        logger.warning(f"Could not detect default branch. Falling back to 'main'. Error: {e}")
        return "main"

def clone_repo(repo_url: str, dest_dir: str):
    """Clones a GitHub repo with optional GitHub token support."""
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        repo_url = repo_url.replace("https://", f"https://{github_token}@")

    return git.Repo.clone_from(repo_url, to_path=dest_dir)

def load_documents_from_github_repo(repo_url: str):
    """Clones a GitHub repo and loads its documents using GitLoader."""
    repo_name = repo_url.rstrip("/").split("/")[-1]
    temp_repo_path = f"temp_{repo_name}"

    if os.path.exists(temp_repo_path):
        logger.info(f"Removing existing temporary repository at {temp_repo_path}...")
        shutil.rmtree(temp_repo_path)

    logger.info(f"Cloning GitHub repository: {repo_url}")
    repo = clone_repo(repo_url, temp_repo_path)
    branch = get_default_branch(repo)

    logger.info(f"Detected branch: {branch}. Loading documents...")
    loader = GitLoader(
        repo_path=temp_repo_path,
        branch=branch,
        file_filter=lambda file_path: file_path.endswith(".py")
    )
    documents = loader.load()

    logger.info(f"Cleaning up temporary repository: {temp_repo_path}")
    shutil.rmtree(temp_repo_path)

    return documents

def load_documents_from_local_directory(directory_path):
    """Loads all .txt files from a local directory as a fallback."""
    logger.info(f"Loading documents from local directory: {directory_path}")
    loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
    return loader.load()

# ----------------------
# Main Logic
# ----------------------

def main():
    logger.info("=== Starting Knowledge Base Setup ===")

    all_documents = []
    if config.GITHUB_REPO_URLS:
        for repo_url in config.GITHUB_REPO_URLS:
            try:
                repo_docs = load_documents_from_github_repo(repo_url)
                all_documents.extend(repo_docs)
            except Exception as e:
                logger.error(f"Failed to load from {repo_url}: {e}")
    else:
        logger.warning("GITHUB_REPO_URLS not set. Falling back to local /mock_data directory.")
        all_documents = load_documents_from_local_directory("mock_data")

    if not all_documents:
        logger.error("No documents loaded. Aborting setup.")
        return

    logger.info(f"Loaded a total of {len(all_documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(all_documents)
    logger.info(f"Split documents into {len(docs)} chunks.")

    logger.info("Initializing embedding model (this may take a moment)...")
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    logger.info(f"Creating vector store in '{config.CHROMA_PERSIST_DIR}'...")
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=config.CHROMA_PERSIST_DIR,
        collection_name=config.CHROMA_COLLECTION_NAME
    )

    logger.info("=== Knowledge Base Setup Complete ===")
    logger.info(f"Vector store persisted in '{config.CHROMA_PERSIST_DIR}'.")

if __name__ == "__main__":
    main()
