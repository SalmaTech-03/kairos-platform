import redis
import pandas as pd
from sqlalchemy import create_engine
import json

class Materializer:
    def __init__(self):
        # 🔌 Connect to Infrastructure
        self.pg_engine = create_engine("postgresql://admin:password@localhost:5432/kairos_core")
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def materialize(self, feature_view_name: str):
        """
        Reads the LATEST values from Postgres and pushes them to Redis.
        """
        print(f"⚡ Starting Materialization for {feature_view_name}...")

        # 1. Query the Offline Store for the LATEST value for each user
        # (In a real system, this runs incrementally. Here we do a full refresh.)
        query = """
        SELECT DISTINCT ON (user_id)
            user_id,
            event_timestamp,
            amount,
            is_fraud
        FROM offline_store.transactions
        ORDER BY user_id, event_timestamp DESC
        """
        
        print(" Fetching latest feature values from Postgres...")
        df = pd.read_sql(query, self.pg_engine)
        print(f" Found {len(df)} unique entities.")

        # 2. Pipeline write to Redis (High Performance)
        print("  Pushing to Redis Online Store...")
        pipeline = self.redis_client.pipeline()
        
        for _, row in df.iterrows():
            # Key Format: "feature_view:entity_id" -> e.g. "transaction_stats:user_1001"
            key = f"{feature_view_name}:{row['user_id']}"
            
            # We store data as a simple Hash Map
            # In production, we would use Protobuf to save space
            mapping = {
                "amount": str(row['amount']),
                "is_fraud": str(row['is_fraud']),
                "timestamp": str(row['event_timestamp'])
            }
            pipeline.hset(key, mapping=mapping)

        # Execute the bulk write
        pipeline.execute()
        print(f" Materialization Complete! {len(df)} keys updated in Redis.")

if __name__ == "__main__":
    mat = Materializer()
    mat.materialize("transaction_stats")