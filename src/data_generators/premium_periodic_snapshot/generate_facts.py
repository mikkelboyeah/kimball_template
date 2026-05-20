import pandas as pd
import numpy as np
from datetime import datetime
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'premium_periodic_snapshot'))
CLAIM_RAW_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'claim_accumulated_snapshot'))
os.makedirs(OUT_DIR, exist_ok=True)

def generate_facts():
    np.random.seed(200)
    random.seed(200)

    # Load existing dimensions to reuse keys
    try:
        df_ph = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_policyholder.parquet'))
        policyholder_ids = df_ph['policyholder_id'].tolist()
    except Exception:
        policyholder_ids = list(range(1000, 1100))

    try:
        df_emp = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_employee.parquet'))
        # Filter for agents if possible, but for mock data we can just take a subset
        agent_ids = df_emp['employee_id'].tolist()
    except Exception:
        agent_ids = list(range(10, 50))

    try:
        df_cov = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_coverage.parquet'))
        coverage_ids = df_cov['coverage_id'].tolist()
    except Exception:
        coverage_ids = list(range(1, 10))

    try:
        df_item = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'dim_covered_item.parquet'))
        covered_item_ids = df_item['covered_item_id'].tolist()
    except Exception:
        covered_item_ids = list(range(10000, 10100))

    # Snapshot dates: End of month for 2023
    snapshot_dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME').strftime('%Y-%m-%d').tolist()

    data = []
    
    # We want "one row per coverage and covered item on a policy each month"
    # To keep it manageable, we'll simulate a set of active combinations
    num_combinations = 500
    combinations = []
    # Use a fixed seed for combination generation to ensure stability
    local_random = random.Random(200)
    for i in range(num_combinations):
        combinations.append({
            'policyholder_id': local_random.choice(policyholder_ids),
            'agent_id': local_random.choice(agent_ids),
            'coverage_id': local_random.choice(coverage_ids),
            'covered_item_id': local_random.choice(covered_item_ids),
            'policy_number': f"POL-{local_random.randint(10000, 99999)}"
        })

    for snapshot_date in snapshot_dates:
        for combo in combinations:
            # Most are active
            status_id = random.choices([1, 2, 3], weights=[0.1, 0.8, 0.1])[0]
            
            written_premium = 0.0
            earned_premium = round(random.uniform(50, 500), 2)
            
            if status_id == 1: # New
                written_premium = round(random.uniform(500, 2000), 2)
            elif status_id == 3: # Cancelled
                written_premium = round(random.uniform(-1000, -200), 2)
                earned_premium = round(earned_premium * 0.5, 2)

            row = combo.copy()
            row.update({
                'month_end_snapshot_date_id': snapshot_date,
                'policy_status_id': status_id,
                'written_premium_revenue_amount': written_premium,
                'earned_premium_revenue_amount': earned_premium
            })
            data.append(row)

    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'fact_premium_periodic_snapshot.parquet'), index=False)
    print(f"Generated {len(df)} rows for fact_premium_periodic_snapshot")

if __name__ == "__main__":
    generate_facts()
