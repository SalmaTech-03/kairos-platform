import os
from google.cloud import bigquery
import pandas as pd

def load_to_bq(csv_path, table_full_id):
    """
    Loads a CSV file into BigQuery.
    Args:
        csv_path: Path to local CSV.
        table_full_id: "project.dataset.table"
    """
    # Ensure Google Creds are set in Env
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(" Warning: GOOGLE_APPLICATION_CREDENTIALS not set.")
    
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    print(f" Uploading {csv_path} to {table_full_id}...")
    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_full_id, job_config=job_config)

    job.result()  # Wait for job to complete
    print(f" Loaded {job.output_rows} rows.")

if __name__ == "__main__":
    load_to_bq("data/creditcard.csv", "kairos-platform.fraud_data.transactions")