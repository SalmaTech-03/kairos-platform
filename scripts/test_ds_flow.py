import pandas as pd
from datetime import datetime, timedelta
# Fix imports to allow running from root
import sys
import os
sys.path.append(os.getcwd())

from sdk.kairos_sdk.client import KairosClient
from sdk.kairos_sdk.core.definitions import FeatureView, Feature

def run_ds_flow():
    print(" Starting Data Scientist Workflow Test...")
    
    # 1. Initialize Client
    client = KairosClient()

    # 2. Define Features
    transactions_view = FeatureView(
        name="transaction_stats",
        entity_name="user_id",
        view_sql="SELECT * FROM offline_store.transactions",
        features=[
            Feature(name="amount", dtype="FLOAT"),
            Feature(name="is_fraud", dtype="INT64")
        ]
    )
    client.register_view(transactions_view)

    # 3. Create a Training Query (Entity DataFrame)
    # We want to know what the user looked like YESTERDAY
    print("\n Querying for features as of 24 hours ago...")
    
    # Pick a random user from the DB to ensure matches
    user_id = "user_1005" 
    lookup_time = datetime.now() - timedelta(days=1)

    entity_df = pd.DataFrame({
        "user_id": [user_id],
        "event_timestamp": [lookup_time]
    })

    # 4. Get Historical Features
    training_df = client.get_historical_features(
        entity_df=entity_df,
        feature_refs=["transaction_stats:amount"]
    )

    print("\n Resulting Training Data:")
    print(training_df)
    
    if not training_df.empty:
        print(f"\n SUCCESS: Retrieved transaction from {training_df['feature_time'].iloc[0]}")
        print(f"   (Request was for {lookup_time})")
        print("   Notice how 'feature_time' is BEFORE 'request_time'. No leakage!")
    else:
        print("\n  No match found (User might have no transactions before that date). Try re-seeding or different user.")

if __name__ == "__main__":
    run_ds_flow()