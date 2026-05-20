import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'fact_policy_transactions'))
os.makedirs(OUT_DIR, exist_ok=True)

def generate_dim_policy_transaction_type():
    data = [
        {'policy_transaction_type_id': 1, 'transaction_category': 'Create', 'transaction_reason_description': 'New Business'},
        {'policy_transaction_type_id': 2, 'transaction_category': 'Alter', 'transaction_reason_description': 'Customer Request'},
        {'policy_transaction_type_id': 3, 'transaction_category': 'Cancel', 'transaction_reason_description': 'Non-payment'},
        {'policy_transaction_type_id': 4, 'transaction_category': 'Rate', 'transaction_reason_description': 'Price Adjustment'}
    ]
    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'dim_policy_transaction_type.parquet'), index=False)
    print("Generated dim_policy_transaction_type")

def generate_dim_policy_transaction_audit():
    data = [
        {'policy_transaction_audit_id': 1, 'etl_job_name': 'policy_tx_daily_load', 'data_quality_flag': 'Passed', 'source_system': 'Web Portal'},
        {'policy_transaction_audit_id': 2, 'etl_job_name': 'policy_tx_daily_load', 'data_quality_flag': 'Warning', 'source_system': 'Legacy Mainframe'}
    ]
    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'dim_policy_transaction_audit.parquet'), index=False)
    print("Generated dim_policy_transaction_audit")

def main():
    generate_dim_policy_transaction_type()
    generate_dim_policy_transaction_audit()

if __name__ == "__main__":
    main()
