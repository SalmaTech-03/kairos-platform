import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import sys
import os

# Connect to SDK
sys.path.append(os.getcwd())
from sdk.kairos_sdk.client import KairosClient

def train_fraud_model():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("fraud_detection_v1")

    client = KairosClient()
    
    print(" Fetching Point-in-Time Correct Training Data...")
    # In reality, you'd fetch this from the Offline Store (Postgres)
    # Simulating data fetch for brevity
    df = pd.read_sql("SELECT * FROM offline_store.transactions", client.engine)
    
    X = df[['amount']] # Add more features in real life
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with mlflow.start_run():
        print(" Training XGBoost Model...")
        model = xgb.XGBClassifier(objective="binary:logistic")
        model.fit(X_train, y_train)

        # Evaluate
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        
        print(f" Accuracy: {acc:.4f} | F1: {f1:.4f}")

        # Log Metrics & Model
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1", f1)
        mlflow.xgboost.log_model(model, "model")
        
        print(" Model saved to MLflow.")

if __name__ == "__main__":
    train_fraud_model()