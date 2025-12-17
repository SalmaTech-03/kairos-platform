import pandas as pd
from sqlalchemy import create_engine

def run_quality_checks():
    print(" Starting Data Quality Checks (Enterprise Mode)...")

    # 1. Connect & Fetch
    db_url = "postgresql://admin:password@localhost:5432/kairos_core"
    print("    Reading data from Postgres...")
    
    try:
        # Fetch the dataframe
        df = pd.read_sql("SELECT * FROM offline_store.transactions", create_engine(db_url))
        print(f" Fetched {len(df)} rows.")
    except Exception as e:
        print(f"    DB Connection Error: {e}")
        return

    # 2. Define Quality Rules
    print(" Running Validation Suite...")
    report = []
    has_errors = False

    #  Rule 1: Completeness (No Null IDs) ---
    null_count = df['transaction_id'].isnull().sum()
    if null_count == 0:
        report.append(" [PASS] Completeness: Transaction IDs are all present.")
    else:
        report.append(f" [FAIL] Completeness: Found {null_count} null IDs.")
        has_errors = True

    # Rule 2: Validity (Amounts must be positive) ---
    # Check for negative amounts or amounts > 1 million
    invalid_amts = df[(df['amount'] < 0) | (df['amount'] > 1000000)]
    if len(invalid_amts) == 0:
        report.append(" [PASS] Validity: All amounts are between $0 and $1M.")
    else:
        report.append(f" [FAIL] Validity: Found {len(invalid_amts)} invalid amounts.")
        has_errors = True

    # --- Rule 3: Consistency (Fraud flag is 0 or 1) ---
    invalid_flags = df[~df['is_fraud'].isin([0, 1])]
    if len(invalid_flags) == 0:
        report.append(" [PASS] Consistency: Fraud flags are strictly 0 or 1.")
    else:
        report.append(f" [FAIL] Consistency: Found {len(invalid_flags)} weird fraud flags.")
        has_errors = True

    # 3. Print Final Report
    print("\n" + "="*40)
    print(" DATA QUALITY REPORT")
    print("="*40)
    for line in report:
        print(line)
    print("="*40)

    if not has_errors:
        print("\n RESULT: Data is clean and ready for ML Training.")
    else:
        print("\n RESULT: Data Quality Issues Detected. Pipeline Stopped.")

if __name__ == "__main__":
    run_quality_checks()