import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'fact_policy_transactions'))
CLAIM_RAW_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'claim_accumulated_snapshot'))
os.makedirs(OUT_DIR, exist_ok=True)

def random_alphanumeric(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_facts(num_rows=10000):
    np.random.seed(100)
    random.seed(100)

    # Try to load existing dimensions from claim_accumulated_snapshot to reuse keys
    policyholder_ids = []
    employee_ids = []
    coverage_ids = []
    covered_item_ids = []

    try:
        df_ph = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_policyholder.parquet'))
        policyholder_ids = df_ph['policyholder_id'].tolist()
    except Exception:
        policyholder_ids = list(range(1000, 9999))

    try:
        df_emp = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_employee.parquet'))
        employee_ids = df_emp['employee_id'].tolist()
    except Exception:
        employee_ids = list(range(10, 999))

    try:
        df_cov = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_coverage.parquet'))
        coverage_ids = df_cov['coverage_id'].tolist()
    except Exception:
        coverage_ids = list(range(1, 20))

    try:
        df_item = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_covered_item.parquet'))
        covered_item_ids = df_item['covered_item_id'].tolist()
    except Exception:
        covered_item_ids = list(range(10000, 99999))

    data = []
    start_date = datetime(2022, 1, 1)

    for i in range(num_rows):
        transaction_date = start_date + timedelta(days=random.randint(0, 730))
        effective_date = transaction_date + timedelta(days=random.randint(0, 30))
        
        # 1-4: specific policy transaction types
        tx_type_id = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.1, 0.2])[0]
        
        # 1-2: explicit audit ids
        tx_audit_id = random.choices([1, 2], weights=[0.9, 0.1])[0]

        policy_number = f"POL-{random.randint(10000, 99999)}"
        tx_number = f"TXN-{100000 + i}"
        
        # Determine amount based on type
        if tx_type_id == 1: # Create
            amount = round(random.uniform(5000, 30000), 2)
        elif tx_type_id == 2: # Alter
            amount = round(random.uniform(-5000, 5000), 2)
        elif tx_type_id == 3: # Cancel
            amount = round(random.uniform(-10000, -1000), 2)
        else: # Rate
            amount = 0.0

        data.append({
            'policy_transaction_date_id': transaction_date.strftime('%Y-%m-%d'),
            'policy_effective_date_id': effective_date.strftime('%Y-%m-%d'),
            'policyholder_id': random.choice(policyholder_ids),
            'employee_id': random.choice(employee_ids),
            'coverage_id': random.choice(coverage_ids),
            'covered_item_id': random.choice(covered_item_ids),
            'policy_transaction_type_id': tx_type_id,
            'policy_transaction_audit_id': tx_audit_id,
            'policy_number': policy_number,
            'policy_transaction_number': tx_number,
            'policy_transaction_amount_nok': amount
        })

    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'fact_policy_transaction.parquet'), index=False)
    print(f"Parquet generated successfully with {num_rows} rows in {OUT_DIR}")

if __name__ == "__main__":
    generate_facts()
