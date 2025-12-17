import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import time

# Connection to the Docker Postgres
# We use 'postgresql' instead of 'postgresql+psycopg2' for broader compatibility
DB_URL = "postgresql://admin:password@localhost:5432/kairos_core"

def generate_data():
    print(" Generating Synthetic Data for Kairos...")
    
    # 1. Generate Users
    user_ids = [f"user_{i}" for i in range(1000, 1100)] # 100 users
    print(f"   👤 Created {len(user_ids)} unique users.")

    # 2. Generate Transactions (History)
    records = []
    base_time = datetime.now() - timedelta(days=30)
    
    print("   Simulating 30 days of transaction history...")
    for _ in range(5000): # 5000 transactions
        u = np.random.choice(user_ids)
        t = base_time + timedelta(minutes=np.random.randint(0, 43200))
        amt = np.round(np.random.exponential(50), 2)
        is_fraud = 1 if (amt > 300 and np.random.random() > 0.8) else 0
        
        description = np.random.choice([
            "Amazon Purchase", "Gas Station", "Uber Ride", "Apple Store", "Starbucks"
        ])

        records.append({
            "transaction_id": f"tx_{np.random.randint(100000,999999)}",
            "user_id": u,
            "event_timestamp": t,
            "amount": amt,
            "description": description,
            "is_fraud": is_fraud
        })

    df = pd.DataFrame(records)
    df = df.sort_values("event_timestamp")

    # 3. Load to Postgres
    print("    Loading into PostgreSQL...")
    engine = create_engine(DB_URL)
    
    # --- FIX IS HERE: Use engine.begin() for automatic transaction handling ---
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS offline_store;"))
    
    # Write DataFrame to SQL
    df.to_sql("transactions", engine, schema="offline_store", if_exists="replace", index=False)
    
    print(f"    Success! {len(df)} rows loaded to 'offline_store.transactions'.")

if __name__ == "__main__":
    generate_data()