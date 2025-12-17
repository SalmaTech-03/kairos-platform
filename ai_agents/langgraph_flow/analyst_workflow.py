import grpc
import sys
import os
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# Connect to SDK paths
sys.path.append(os.getcwd())
from sdk.kairos_sdk.core import kairos_pb2, kairos_pb2_grpc

def get_real_data(user_id):
    """Tool: Fetches actual data from Go/Redis"""
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = kairos_pb2_grpc.FeatureStoreServiceStub(channel)
        req = kairos_pb2.GetOnlineFeaturesRequest(
            feature_view_name="transaction_stats",
            entity_id=user_id,
            feature_names=["amount", "is_fraud", "timestamp"]
        )
        resp = stub.GetOnlineFeatures(req)
        return resp.values
    except:
        return None

def run_real_agent():
    print(" Initializing Local Llama 3 Agent...")
    
    # 1. Connect to Local LLM
    try:
        llm = ChatOllama(model="llama3", temperature=0)
    except:
        print(" Error: Is Ollama running? Run 'ollama run llama3' in a separate terminal.")
        return

    print("   Ready. Ask me about a user (e.g. 'Audit user_1001'). Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]: break

        # 2. Logic: Extract User ID manually (to save token complexity for this demo)
        # In a full LangGraph, the LLM would do this tool calling itself.
        import re
        match = re.search(r"user_\d+", user_input)
        
        context_data = ""
        if match:
            uid = match.group(0)
            print(f"   ( Agent detected {uid}, fetching live data...)")
            data = get_real_data(uid)
            if data:
                context_data = f"DATA CONTEXT FOR {uid}: Amount=${data.get('amount')}, FraudFlag={data.get('is_fraud')}, Time={data.get('timestamp')}"
            else:
                context_data = f"DATA CONTEXT: User {uid} not found in database."

        # 3. Prompt the Real AI
        # We inject the Real Data into the prompt so the AI can "Reason" about it.
        prompt = f"""
        You are a Senior Fraud Analyst. 
        User Question: "{user_input}"
        
        {context_data}
        
        If you have data, analyze it. 
        - If FraudFlag is 1, be alarmed. 
        - If Amount > 200, mention it's high.
        - If no data, say so.
        Keep it professional and concise.
        """
        
        print("   ( Llama 3 is thinking...)")
        response = llm.invoke([HumanMessage(content=prompt)])
        print(f"AI: {response.content}")

if __name__ == "__main__":
    run_real_agent()