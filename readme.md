# ==============================================================================
# File: README.md
# Description: Instructions for setting up and running the project.
# ==============================================================================
"""
# AI-Powered Jira Story Generator (Multi-Repo Edition)

This project implements the complete workflow for transforming a one-liner user prompt
into a detailed, context-aware story. It uses a RAG pipeline with Google's Gemini model
and can pull context from multiple public GitHub repositories to create a unified knowledge base.

This version runs entirely offline. It writes its output to a local file (`output.md`)
instead of creating a Jira ticket.

## Project Structure

```
/jira_story_generator
|
|-- main.py                 # 1. Input Interface (FastAPI) & Orchestration Trigger
|-- orchestration_service.py  # 2. Orchestration Service (Core Logic)
|-- knowledge_base_manager.py # 3. Knowledge Base (Setup Script from GitHub or local data)
|-- context_retrieval.py      # 4. Context Retrieval Engine
|-- llm_interface.py          # 5. GenAI Model Interface (Gemini)
|-- jira_integration.py       # 6. Post-Processing & Output File Generation
|
|-- config.py               # Configuration for API keys and settings
|-- requirements.txt        # Project dependencies
|-- .env                    # Environment variables (needs to be created)
|-- output.md               # The generated story will be saved here
|
|-- templates/              # Web interface files
|   |-- index.html
|
|-- mock_data/              # Fallback sample documents
|   |-- api_docs.txt
|   |-- design_system.txt
|   |-- existing_stories.txt
```

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Git installed on your system.
- A Google AI API key for Gemini (from Google AI Studio).

### 2. Clone the Repository & Install Dependencies
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a file named `.env` in the project root and add your credentials:

```ini
# .env file

# Google AI API Key
GOOGLE_API_KEY="your_google_ai_api_key"

# --- GitHub Configuration ---
# Point this to a comma-separated list of public GitHub repositories.
# If left blank, it will use the local /mock_data directory as a fallback.
# Example: GITHUB_REPO_URLS="[https://github.com/pallets/flask,https://github.com/tiangolo/fastapi](https://github.com/pallets/flask,https://github.com/tiangolo/fastapi)"
GITHUB_REPO_URLS="[https://github.com/pallets/flask,https://github.com/tiangolo/fastapi](https://github.com/pallets/flask,https://github.com/tiangolo/fastapi)"
```

### 4. Build the Knowledge Base
Before running the main application, you need to populate the vector database. This script will clone the specified GitHub repos (or use local data), create embeddings from the content, and store them locally.

**Run this script once:**
```bash
python knowledge_base_manager.py
```
You should see output indicating that the knowledge base has been created successfully.

### 5. Run the Application
Start the FastAPI server. This provides the input interface.

```bash
uvicorn main:app --reload
```
The server will be running at `http://127.0.0.1:8000`.

### 6. Usage
Navigate to `http://127.0.0.1:8000` in your browser. You will see the web interface where you can enter your one-liner prompt. After generation, check the `output.md` file in your project directory for the result.
"""