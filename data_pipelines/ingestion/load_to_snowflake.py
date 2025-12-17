import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import os

def load_to_snowflake(csv_path, table_name):
    # Retrieve credentials from env
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    
    ctx = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse="COMPUTE_WH",
        database="KAIROS_DB",
        schema="PUBLIC"
    )
    
    df = pd.read_csv(csv_path)
    
    print(f" Uploading to Snowflake Table: {table_name}")
    success, n_chunks, n_rows, _ = write_pandas(ctx, df, table_name)
    
    print(f" Success: Uploaded {n_rows} rows.")
    ctx.close()

if __name__ == "__main__":
    load_to_snowflake("data/creditcard.csv", "TRANSACTIONS")