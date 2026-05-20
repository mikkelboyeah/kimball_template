import pandas as pd
import numpy as np
from datetime import datetime
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'claim_periodic_snapshot'))
CLAIM_RAW_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'claim_accumulated_snapshot'))
os.makedirs(OUT_DIR, exist_ok=True)

def generate_facts():
    np.random.seed(300)
    random.seed(300)

    # Load existing claims and their associated dimension keys
    try:
        # First, try to load premium snapshot to align policy combinations
        PREM_RAW_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'premium_periodic_snapshot'))
        df_prem = pd.read_parquet(os.path.join(PREM_RAW_DIR, 'fact_premium_periodic_snapshot.parquet'))
        
        # Get unique policy combinations from premium snapshot
        policy_combos = df_prem[['policyholder_id', 'agent_id', 'coverage_id', 'covered_item_id', 'policy_number']].drop_duplicates().to_dict('records')
        
        df_acc = pd.read_parquet(os.path.join(CLAIM_RAW_DIR, 'claim_accumulating_snapshot.parquet'))
        # We'll use a subset of claims but assign them aligned policy info
        acc_claims = df_acc[['claim_id', 'claim_supervisor_id', 'claimant_id', 'claim_status_id', 'claim_profile_id']].head(200).to_dict('records')
        
        claims = []
        for i, acc_claim in enumerate(acc_claims):
            # Assign a policy combo from the premium snapshot to each claim
            combo = policy_combos[i % len(policy_combos)]
            claim = acc_claim.copy()
            claim.update(combo)
            claims.append(claim)

    except Exception as e:
        print(f"Warning: Could not align with premium snapshot or legacy claims: {e}")
        claims = []
        for i in range(1, 101):
            claims.append({
                'claim_id': i,
                'policyholder_id': random.randint(1000, 1100),
                'claim_supervisor_id': random.randint(1, 10),
                'agent_id': random.randint(10, 50),
                'coverage_id': random.randint(1, 10),
                'covered_item_id': random.randint(10000, 10100),
                'claimant_id': random.randint(1, 100),
                'claim_status_id': random.randint(1, 5),
                'claim_profile_id': random.randint(1, 10),
                'policy_number': f'POL-{random.randint(10000, 99999)}'
            })

    # Snapshot dates: End of month for 2023
    snapshot_dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME').strftime('%Y-%m-%d').tolist()

    data = []

    for snapshot_date in snapshot_dates:
        for claim in claims:
            # Randomly decide if the claim is active this month
            if random.random() > 0.3:
                amount_claimed = round(random.uniform(0, 5000), 2)
                amount_paid = round(random.uniform(0, amount_claimed), 2)
                change_in_reserve = round(random.uniform(-1000, 1000), 2)
                current_reserve_balance = round(random.uniform(0, 10000), 2) # Simulate semi-additive reserve balance

                row = claim.copy()
                row.update({
                    'month_end_snapshot_date_id': snapshot_date,
                    'amount_claimed': amount_claimed,
                    'amount_paid': amount_paid,
                    'change_in_reserve': change_in_reserve,
                    'current_reserve_balance': current_reserve_balance,
                    'claim_number': f'CLM-{row["claim_id"]}' # Generate claim number from claim_id
                })
                data.append(row)

    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'fact_claim_periodic_snapshot.parquet'), index=False)
    print(f"Generated {len(df)} rows for fact_claim_periodic_snapshot")

if __name__ == "__main__":
    generate_facts()
