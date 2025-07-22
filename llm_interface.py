# ==============================================================================
# File: llm_interface.py
# Component: 5. GenAI Model (LLM) Interface
# ==============================================================================
import google.generativeai as genai
import config
import json

def generate_story_from_prompt(master_prompt: str) -> dict:
    """
    Calls the Gemini API to generate the Jira story based on the master prompt.
    """
    print("--- Calling GenAI Model (Gemini) ---")
    genai.configure(api_key=config.GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    # Instruct the model to generate a JSON object
    generation_config = genai.types.GenerationConfig(response_mime_type="application/json")

    try:
        response = model.generate_content(master_prompt, generation_config=generation_config)
        print("--- GenAI Model response received ---")
        
        # The response text should be a valid JSON string
        response_json = json.loads(response.text)
        return response_json
        
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        # Return a structured error
        return {
            "error": "Failed to generate story from LLM.",
            "details": str(e)
        }
