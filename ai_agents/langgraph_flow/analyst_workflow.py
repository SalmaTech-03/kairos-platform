import os
import sys
import grpc
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Fix path for imports
sys.path.append(os.getcwd())
from sdk.kairos_sdk.core import kairos_pb2, kairos_pb2_grpc

# --- 1. Define the Feature Store Tool ---
def get_user_stats(user_id: str):
    """
    Fetches real-time transaction stats for a user from the Kairos Feature Store.
    """
    print(f"   [Tool] AI is calling Go Server for {user_id}...")
    
    channel = grpc.insecure_channel('localhost:50051')
    stub = kairos_pb2_grpc.FeatureStoreServiceStub(channel)
    
    try:
        req = kairos_pb2.GetOnlineFeaturesRequest(
            feature_view_name="transaction_stats",
            entity_id=user_id,
            feature_names=["amount", "is_fraud", "timestamp"]
        )
        resp = stub.GetOnlineFeatures(req)
        return str(resp.values) # Return data as string for the LLM
    except Exception as e:
        return f"Error: {str(e)}"

# --- 2. The Agent Logic (The Brain) ---
class AgentState(TypedDict):
    messages: list[str]

def analyst_node(state: AgentState):
    """
    Decides whether to call the tool or answer.
    """
    last_message = state['messages'][-1]
    
    # Simple Keyword Logic (Simulating an LLM decision)
    if "user_" in last_message and "check" in last_message.lower():
        # Extract user_id (simple parsing)
        words = last_message.split()
        user_id = next((w for w in words if w.startswith("user_")), None)
        
        if user_id:
            # CALL THE TOOL
            data = get_user_stats(user_id)
            
            # GENERATE INSIGHT
            if "'is_fraud': '1'" in data:
                insight = f" ALERT: {user_id} has a fraud flag! Transaction amount: {data}."
            else:
                insight = f" CLEAN: {user_id} looks safe. Recent activity: {data}."
            
            return {"messages": state['messages'] + [insight]}
    
    return {"messages": state['messages'] + ["I need a user ID (e.g., user_1001) to check for fraud."]}

# --- 3. Build the Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("analyst", analyst_node)
workflow.set_entry_point("analyst")
workflow.add_edge("analyst", END)

app = workflow.compile()

# --- 4. Run the Chat Loop ---
if __name__ == "__main__":
    print(" Kairos AI Analyst Ready! (Type 'quit' to exit)")
    print("   Try asking: 'Check user_1001 please'")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        result = app.invoke({"messages": [user_input]})
        print(f"AI:  {result['messages'][-1]}")