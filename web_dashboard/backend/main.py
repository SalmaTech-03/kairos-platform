from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import grpc
import re

# Add SDK to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from sdk.kairos_sdk.core import kairos_pb2, kairos_pb2_grpc

app = FastAPI(title="Kairos Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class FeatureRequest(BaseModel):
    user_id: str

# Helper: Get Real Data from Go
def fetch_from_go(user_id: str):
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

@app.post("/api/inference")
def get_features(req: FeatureRequest):
    data = fetch_from_go(req.user_id)
    if not data: return {"error": "No data found"}
    return data

@app.get("/api/registry")
def get_registry():
    return {"feature_views": [{"name": "transaction_stats", "entity": "user_id", "features": ["amount", "is_fraud", "timestamp"]}]}

@app.post("/api/chat")
def chat_agent(req: ChatRequest):
    msg = req.message.lower()
    
    # --- LOGIC: Only check data if a user ID is found ---
    user_match = re.search(r"user_\d+", msg)

    if user_match:
        user_id = user_match.group(0)
        data = fetch_from_go(user_id)
        
        if not data:
            return {"response": f"⚠️ I looked for **{user_id}** in Redis, but found nothing. (Did you run 'make seed'?)"}
        
        amount = float(data.get("amount", 0.0))
        is_fraud = int(data.get("is_fraud", 0))
        timestamp = data.get("timestamp", "N/A")
        
        risk = "HIGH" if is_fraud == 1 else "LOW"
        reason = "Fraud flag is TRUE." if is_fraud == 1 else "Transaction looks normal."

        response = (f"📊 **Real-Time Data for {user_id}:**\n"
                    f"- Spend: ${amount}\n"
                    f"- Time: {timestamp}\n\n"
                    f"🤖 **Verdict:** Risk is **{risk}**.\n"
                    f"Reason: {reason}")
        
    elif "hai" in msg or "hello" in msg or "hi" in msg:
        response = " **Hello!** I am the Kairos AI. Please give me a User ID (e.g. 'Check user_1001') to analyze."
        
    else:
        response = "I didn't understand. Try asking: **'Check user_1001'**"

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)