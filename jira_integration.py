# ==============================================================================
# File: jira_integration.py
# Component: 6. Post-Processing & Output File Generation
# ==============================================================================
# from jira import JIRA # Commented out
import config

def create_story_output_file(story_data: dict) -> str:
    """
    Writes the generated story to a local markdown file instead of creating a Jira ticket.
    """
    print("--- Generating output.md file ---")
    
    # Perform basic validation (Post-Processing)
    required_keys = ["title", "user_story", "acceptance_criteria"]
    if not all(key in story_data for key in required_keys):
        raise ValueError("Generated story data is missing required keys.")

    try:
        # Format the description field for Markdown
        story_points = story_data.get('story_points', 'N/A')
        
        output_content = f"""
# {story_data['title']}

**Story Points:** {story_points}

---

## User Story
{story_data['user_story']}

## Acceptance Criteria
{story_data['acceptance_criteria']}
"""
        output_filename = "output.md"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(output_content)
            
        print(f"--- Successfully created {output_filename} ---")
        return output_filename

    except Exception as e:
        print(f"An error occurred while creating output file: {e}")
        raise
