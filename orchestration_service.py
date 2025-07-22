# ==============================================================================
# File: orchestration_service.py
# Component: 2. Orchestration Service
# ==============================================================================
from context_retrieval import retrieve_context
from llm_interface import generate_story_from_prompt
from jira_integration import create_story_output_file

def build_master_prompt(user_prompt: str, context: str) -> str:
    """
    Constructs the final, detailed prompt for the GenAI model,
    including the user prompt, retrieved context, and few-shot examples.
    """
    master_prompt = f"""
    You are an expert Agile Business Analyst. Your task is to convert a user's one-line requirement into a detailed, well-structured Jira story.

    Follow these instructions carefully:
    1.  Analyze the user's request and the provided context from our internal documentation.
    2.  Generate a response in a valid JSON format. The JSON object must contain the following keys: "title", "user_story", "acceptance_criteria", and "story_points".
    3.  The "title" should be a concise, descriptive summary.
    4.  The "user_story" should follow the format: "As a [persona], I want to [action] so that [benefit]."
    5.  The "acceptance_criteria" should be a bulleted list (using hyphens) of testable conditions.
    6.  The "story_points" must be an integer from the Fibonacci sequence (1, 2, 3, 5, 8, 13).
    7.  Base your response on the provided context. If the context mentions specific components or API endpoints, refer to them.

    --- CONTEXT FROM KNOWLEDGE BASE ---
    {context}
    --- END OF CONTEXT ---

    --- FEW-SHOT EXAMPLE ---
    User Request: "Add avatar upload"
    JSON Response Example:
    {{
        "title": "User Profile - Add Avatar Upload Functionality",
        "user_story": "As a registered user, I want to upload and change my profile avatar so that I can personalize my account identity.",
        "acceptance_criteria": "- Given I am on my profile page, when I click on the default avatar, then a file selection dialog should open.\\n- Given I have selected a valid image file (JPG, PNG) under 5MB, when I confirm the selection, then the image should be uploaded and displayed as my new avatar.\\n- Given the upload is in progress, a loading indicator should be shown over the avatar.",
        "story_points": 5
    }}
    --- END OF EXAMPLE ---

    Now, generate the Jira story for the following user request.

    --- USER REQUEST ---
    {user_prompt}
    --- END OF USER REQUEST ---

    Provide only the JSON object in your response.
    """
    return master_prompt

def process_new_story_request(user_prompt: str) -> str:
    """
    Manages the entire workflow from prompt to output file creation.
    """
    # 1. Retrieve context from the knowledge base
    context = retrieve_context(user_prompt)

    # 2. Construct the master prompt
    master_prompt = build_master_prompt(user_prompt, context)

    # 3. Call the GenAI model
    generated_story_data = generate_story_from_prompt(master_prompt)
    
    if "error" in generated_story_data:
        raise Exception(f"Failed to generate story: {generated_story_data['details']}")

    # 4. Post-process and create the output file
    output_file_path = create_story_output_file(generated_story_data)

    return output_file_path
