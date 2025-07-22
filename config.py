# ==============================================================================
# File: config.py
# Description: Loads configuration from environment variables.
# ==============================================================================
import os
from dotenv import load_dotenv

load_dotenv()

# Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Jira (Credentials are no longer used but kept for potential future use)
JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Confluence (Credentials are no longer used but kept for potential future use)
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")


# ChromaDB settings
CHROMA_PERSIST_DIR = "chroma_db"
CHROMA_COLLECTION_NAME = "jira_knowledge_base"