import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import os

# Determine the output directory relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'claim_accumulated_snapshot'))
os.makedirs(RAW_DIR, exist_ok=True)

def random_alphanumeric(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_unique_keys(df_fact, column_name):
    # Filter out empty or placeholder values
    unique_vals = df_fact[column_name].dropna().unique()
    return unique_vals

def generate_dim_date(df_fact):
    # Collect all dates used in the fact table across all date columns
    date_columns = [
        'claim_open_date_id', 'claim_accident_date_id', 'claim_estimate_date_id',
        'claim_1st_payment_date_id', 'claim_most_recent_payment_date_id',
        'claim_subrogation_date_id', 'claim_close_date_id'
    ]
    all_dates = pd.concat([df_fact[col] for col in date_columns]).dropna().unique()
    
    dates_df = pd.DataFrame({'full_date': all_dates})
    
    # Filter out 9999-12-31 to handle properly
    dates_df = dates_df[dates_df['full_date'] != '9999-12-31'].copy()
    
    min_date = pd.to_datetime(dates_df['full_date']).min()
    max_date = pd.to_datetime('today').normalize() # Up to today
    
    if pd.isna(min_date):
        min_date = max_date - pd.DateOffset(years=5)
    else:
        min_date = min(min_date, max_date - pd.DateOffset(years=5))
        
    dates_rng = pd.date_range(start=min_date, end=max_date, freq='D')
    
    df = pd.DataFrame({'full_date': dates_rng})
    # date_id is same as full_date string (YYYY-MM-DD) to match the fact table
    df['date_id'] = df['full_date'].dt.strftime('%Y-%m-%d')
    df['full_date'] = df['full_date'].dt.strftime('%Y-%m-%d')
    df['year'] = pd.to_datetime(df['full_date']).dt.year
    df['month'] = pd.to_datetime(df['full_date']).dt.month
    df['month_name'] = pd.to_datetime(df['full_date']).dt.strftime('%B')
    df['quarter'] = 'Q' + pd.to_datetime(df['full_date']).dt.quarter.astype(str)
    df['day_of_week'] = pd.to_datetime(df['full_date']).dt.strftime('%A')
    df['is_weekend'] = np.where(pd.to_datetime(df['full_date']).dt.dayofweek >= 5, 'Yes', 'No')
    df['is_holiday'] = np.random.choice(['Yes', 'No'], size=len(df), p=[0.03, 0.97])
    
    # 9999-12-31 placeholder
    placeholder = {
        'date_id': '9999-12-31',
        'full_date': '9999-12-31',
        'year': 9999,
        'month': 12,
        'month_name': 'Unknown',
        'quarter': 'Unknown',
        'day_of_week': 'Unknown',
        'is_weekend': 'Unknown',
        'is_holiday': 'Unknown'
    }
    df = pd.concat([df, pd.DataFrame([placeholder])], ignore_index=True)
    df = df[['date_id', 'full_date', 'year', 'month', 'month_name', 'quarter', 'day_of_week', 'is_weekend', 'is_holiday']]
    
    # Also ensure any straggler dates from the fact table are included in dim_date
    missing_dates = set(all_dates) - set(df['date_id'].values)
    if missing_dates:
        missing_df = pd.DataFrame({'date_id': list(missing_dates)})
        missing_df['full_date'] = missing_df['date_id']
        missing_df['year'] = pd.to_datetime(missing_df['full_date']).dt.year
        missing_df['month'] = pd.to_datetime(missing_df['full_date']).dt.month
        missing_df['month_name'] = pd.to_datetime(missing_df['full_date']).dt.strftime('%B')
        missing_df['quarter'] = 'Q' + pd.to_datetime(missing_df['full_date']).dt.quarter.astype(str)
        missing_df['day_of_week'] = pd.to_datetime(missing_df['full_date']).dt.strftime('%A')
        missing_df['is_weekend'] = np.where(pd.to_datetime(missing_df['full_date']).dt.dayofweek >= 5, 'Yes', 'No')
        missing_df['is_holiday'] = 'No'
        df = pd.concat([df, missing_df], ignore_index=True)
        
    df.to_parquet(os.path.join(RAW_DIR, 'dim_date.parquet'), index=False)

def generate_dim_policyholder(fact_keys):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'policyholder_id': fact_keys})
    df['policyholder_natural_id'] = [f"PH-{random_alphanumeric(6)}" for _ in range(NUM_ROWS)]
    df['first_name'] = [random.choice(["John", "Jane", "Alice", "Bob", "Charlie", "Diana"]) for _ in range(NUM_ROWS)]
    df['last_name'] = [random.choice(["Smith", "Doe", "Johnson", "Davis", "Miller", "Wilson"]) for _ in range(NUM_ROWS)]
    df['city'] = [random.choice(["New York", "Chicago", "Houston", "Phoenix", "Philadelphia"]) for _ in range(NUM_ROWS)]
    df['state'] = [random.choice(["NY", "IL", "TX", "AZ", "PA"]) for _ in range(NUM_ROWS)]
    df['zip_code'] = [f"{random.randint(10000, 99999)}" for _ in range(NUM_ROWS)]
    df['customer_segment'] = [random.choice(["Standard", "Preferred", "High Risk"]) for _ in range(NUM_ROWS)]
    df.to_parquet(os.path.join(RAW_DIR, 'dim_policyholder.parquet'), index=False)

def generate_dim_coverage(fact_keys):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'coverage_id': fact_keys})
    df['coverage_code'] = [f"CVG-{random_alphanumeric(4)}" for _ in range(NUM_ROWS)]
    df['line_of_business'] = [random.choice(["Auto", "Home", "Renters"]) for _ in range(NUM_ROWS)]
    df['coverage_type'] = np.where(df['line_of_business'] == 'Auto', 
                                   [random.choice(["Collision", "Liability", "Comprehensive"]) for _ in range(NUM_ROWS)],
                                   [random.choice(["Fire", "Liability", "Water Damage"]) for _ in range(NUM_ROWS)])
    df['deductible_amount'] = [random.choice([250, 500, 1000, 2000, 5000]) for _ in range(NUM_ROWS)]
    df['coverage_limit'] = [random.choice([50000, 100000, 300000, 500000, 1000000]) for _ in range(NUM_ROWS)]
    df.to_parquet(os.path.join(RAW_DIR, 'dim_coverage.parquet'), index=False)

def generate_dim_claimant(fact_keys):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'claimant_id': fact_keys})
    df['claimant_natural_id'] = [f"CLMT-{random_alphanumeric(6)}" for _ in range(NUM_ROWS)]
    df['first_name'] = [random.choice(["Sam", "Chris", "Pat", "Alex", "Taylor"]) for _ in range(NUM_ROWS)]
    df['last_name'] = [random.choice(["Brown", "Jones", "Garcia", "Martinez", "Rodriguez"]) for _ in range(NUM_ROWS)]
    df['relationship_to_policyholder'] = [random.choice(["Self", "Spouse", "Third Party", "Child"]) for _ in range(NUM_ROWS)]
    df.to_parquet(os.path.join(RAW_DIR, 'dim_claimant.parquet'), index=False)

def generate_dim_claim_profile(fact_keys):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'claim_profile_id': fact_keys})
    df['catastrophe_indicator'] = [random.choice(["Yes", "No"]) for _ in range(NUM_ROWS)]
    df['police_report_filed'] = [random.choice(["Yes", "No"]) for _ in range(NUM_ROWS)]
    df['claim_report_method'] = [random.choice(["Phone", "Mobile App", "Web", "Agent"]) for _ in range(NUM_ROWS)]
    df.to_parquet(os.path.join(RAW_DIR, 'dim_claim_profile.parquet'), index=False)

def generate_dim_employee(agent_keys, supervisor_keys):
    fact_keys = list(set(agent_keys) | set(supervisor_keys))
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'employee_id': fact_keys})
    df['employee_natural_id'] = [f"EMP-{random_alphanumeric(5)}" for _ in range(NUM_ROWS)]
    df['first_name'] = [random.choice(["Michael", "Sarah", "David", "Laura", "James"]) for _ in range(NUM_ROWS)]
    df['last_name'] = [random.choice(["Anderson", "Thomas", "Jackson", "White", "Harris"]) for _ in range(NUM_ROWS)]
    df['job_title'] = [random.choice(["Agent", "Claim Supervisor"]) for _ in range(NUM_ROWS)]
    df['region'] = [random.choice(["North", "South", "East", "West", "Central"]) for _ in range(NUM_ROWS)]
    df.to_parquet(os.path.join(RAW_DIR, 'dim_employee.parquet'), index=False)

def generate_dim_covered_item(fact_keys):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'covered_item_id': fact_keys})
    df['item_type'] = [random.choice(["Vehicle", "Property"]) for _ in range(NUM_ROWS)]
    df['item_description'] = np.where(df['item_type'] == 'Vehicle',
                                      [random.choice(["2018 Toyota Camry", "2020 Ford F-150", "2015 Honda Accord"]) for _ in range(NUM_ROWS)],
                                      [random.choice(["Single Family Home", "Townhouse", "Condominium"]) for _ in range(NUM_ROWS)])
    df['appraised_value_range'] = np.where(df['item_type'] == 'Vehicle',
                                           [random.choice(["Under 20k", "20k-50k", "Over 50k"]) for _ in range(NUM_ROWS)],
                                           [random.choice(["Under 200k", "200k-500k", "Over 500k"]) for _ in range(NUM_ROWS)])
    df.to_parquet(os.path.join(RAW_DIR, 'dim_covered_item.parquet'), index=False)

def generate_dim_claim_status(fact_keys):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({'claim_status_id': fact_keys})
    df['status_description'] = [random.choice(["Open", "Closed", "Reopened", "Denied"]) for _ in range(NUM_ROWS)]
    df['sub_status_description'] = np.where(df['status_description'] == 'Open',
                                            [random.choice(["Pending Estimate", "Awaiting Payment"]) for _ in range(NUM_ROWS)],
                                            [random.choice(["Resolved", "Finalized"]) for _ in range(NUM_ROWS)])
    df.to_parquet(os.path.join(RAW_DIR, 'dim_claim_status.parquet'), index=False)

def generate_dim_claim(fact_keys, claim_numbers):
    NUM_ROWS = len(fact_keys)
    df = pd.DataFrame({
        'claim_id': fact_keys,
        'claim_number': claim_numbers
    })
    df['loss_description'] = [random.choice(["Rear-end collision", "Hail damage", "Water leak", "Fire damage", "Theft"]) for _ in range(NUM_ROWS)]
    df['fault_indicator'] = [random.choice(["Insured At Fault", "Third Party At Fault", "No Fault", "Unknown"]) for _ in range(NUM_ROWS)]
    df.to_parquet(os.path.join(RAW_DIR, 'dim_claim.parquet'), index=False)

def main():
    np.random.seed(42)
    random.seed(42)
    
    fact_parquet = os.path.join(RAW_DIR, 'claim_accumulating_snapshot.parquet')
    df_fact = pd.read_parquet(fact_parquet)
    
    generate_dim_date(df_fact)
    generate_dim_policyholder(get_unique_keys(df_fact, "policyholder_id"))
    generate_dim_coverage(get_unique_keys(df_fact, "coverage_id"))
    generate_dim_claimant(get_unique_keys(df_fact, "claimant_id"))
    generate_dim_claim_profile(get_unique_keys(df_fact, "claim_profile_id"))
    
    agent_keys = get_unique_keys(df_fact, "agent_id")
    supervisor_keys = get_unique_keys(df_fact, "claim_supervisor_id")
    generate_dim_employee(agent_keys, supervisor_keys)
    
    generate_dim_covered_item(get_unique_keys(df_fact, "covered_item_id"))
    generate_dim_claim_status(get_unique_keys(df_fact, "claim_status_id"))
    
    # Claim Number is usually alphanumeric in fact, if available. Let's check headers:
    claim_keys = get_unique_keys(df_fact, "claim_id")
    claim_numbers = [f"CLM-{random_alphanumeric(8)}" for _ in range(len(claim_keys))]
    generate_dim_claim(claim_keys, claim_numbers)
    
    print(f"Successfully generated all 9 dimension parquet files in {RAW_DIR}")

if __name__ == "__main__":
    main()
