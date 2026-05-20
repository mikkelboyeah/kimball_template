import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'premium_periodic_snapshot'))
os.makedirs(OUT_DIR, exist_ok=True)

def generate_dim_policy_status():
    data = [
        {'policy_status_id': 1, 'status_name': 'New', 'status_description': 'Recently issued policy'},
        {'policy_status_id': 2, 'status_name': 'Active', 'status_description': 'In-force policy'},
        {'policy_status_id': 3, 'status_name': 'Cancelled', 'status_description': 'Terminated policy'}
    ]
    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'dim_policy_status.parquet'), index=False)
    print("Generated dim_policy_status")

def main():
    generate_dim_policy_status()

if __name__ == "__main__":
    main()
