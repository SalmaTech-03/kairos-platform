import autogen
import os

def get_sql_agent():
    # Load API Key from Environment
    api_key = os.getenv("OPENAI_API_KEY", "your-key-here")
    
    config_list = [{"model": "gpt-4", "api_key": api_key}]
    
    return autogen.AssistantAgent(
        name="SQL_Expert",
        llm_config={"config_list": config_list},
        system_message="""
        You are a Senior Data Engineer specializing in BigQuery and PostgreSQL.
        Your goal is to write efficient SQL queries to extract feature data.
        
        Schema 'transactions':
        - transaction_id (STRING)
        - user_id (STRING)
        - amount (FLOAT)
        - is_fraud (INT)
        - event_timestamp (TIMESTAMP)
        
        Rules:
        1. Always use standard SQL.
        2. Always filter by `event_timestamp` to prevent scanning the whole table.
        3. Output ONLY the SQL code block.
        """
    )