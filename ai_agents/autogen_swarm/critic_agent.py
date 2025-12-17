import autogen
import os

def get_critic_agent():
    api_key = os.getenv("OPENAI_API_KEY", "your-key-here")
    config_list = [{"model": "gpt-4", "api_key": api_key}]

    return autogen.AssistantAgent(
        name="Code_Critic",
        llm_config={"config_list": config_list},
        system_message="""
        You are a Database Administrator. Review the SQL output from the SQL_Expert.
        
        Check for:
        1. Syntax errors.
        2. Missing WHERE clauses (Safety check).
        3. Potential injection risks.
        
        If the SQL is safe and correct, reply exactly: "APPROVED".
        If there are issues, list them clearly.
        """
    )