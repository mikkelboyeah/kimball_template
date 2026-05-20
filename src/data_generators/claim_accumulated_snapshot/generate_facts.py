import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_mock_data(num_rows=5000):
    np.random.seed(42)
    random.seed(42)

    # Business Rules
    CLOSED_RATIO = 0.8
    SUBRO_SALVAGE_RATIO = 0.1
    DEFAULT_DATE = '9999-12-31'

    data = []

    start_date = datetime(2023, 1, 1)

    for i in range(num_rows):
        is_closed = random.random() < CLOSED_RATIO
        has_subro_salvage = random.random() < SUBRO_SALVAGE_RATIO

        # Randomize Accident Date within the last 3 years
        accident_date = start_date + timedelta(days=random.randint(0, 1000))
        
        # Chronological Progression
        open_date = accident_date + timedelta(days=random.randint(0, 30))
        estimate_date = open_date + timedelta(days=random.randint(1, 14))
        first_payment_date = estimate_date + timedelta(days=random.randint(2, 60))
        
        if is_closed:
            most_recent_payment_date = first_payment_date + timedelta(days=random.randint(0, 180))
            close_date = most_recent_payment_date + timedelta(days=random.randint(1, 30))
        else:
            # For open claims, some might have payments, some not
            if random.random() < 0.7:
                most_recent_payment_date = first_payment_date + timedelta(days=random.randint(0, 90))
            else:
                first_payment_date = datetime(9999, 12, 31)
                most_recent_payment_date = datetime(9999, 12, 31)
            close_date = datetime(9999, 12, 31)

        # Subrogation Date (10% chance)
        if has_subro_salvage and first_payment_date.year != 9999:
            subrogation_date = first_payment_date + timedelta(days=random.randint(30, 120))
        else:
            subrogation_date = datetime(9999, 12, 31)

        # Ensure most_recent_payment is not unknown if first_payment is known
        if first_payment_date.year != 9999 and most_recent_payment_date.year == 9999:
             most_recent_payment_date = first_payment_date

        # Format dates as YYYY-MM-DD
        def format_date(d):
            return d.strftime('%Y-%m-%d') if d.year != 9999 else DEFAULT_DATE

        # Financials in NOK
        original_reserve = round(random.uniform(5000, 500000), 2)
        estimate_nok = round(original_reserve * random.uniform(0.8, 1.2), 2)
        
        if is_closed:
            paid_to_date = estimate_nok
            current_reserve = 0.0
        else:
            # If not closed, paid some portion
            if first_payment_date.year == 9999:
                paid_to_date = 0.0
            else:
                paid_to_date = round(estimate_nok * random.uniform(0.1, 0.9), 2)
            current_reserve = round(estimate_nok - paid_to_date, 2)

        salvage_collected = 0.0
        subro_collected = 0.0
        if has_subro_salvage and paid_to_date > 0:
            salvage_collected = round(paid_to_date * random.uniform(0.01, 0.1), 2)
            subro_collected = round(paid_to_date * random.uniform(0.01, 0.2), 2)

        # Lag Calculations
        def calc_lag(d1, d2):
            if d1.year == 9999 or d2.year == 9999:
                return 0
            return (d2 - d1).days

        accident_to_open_lag = calc_lag(accident_date, open_date)
        open_to_estimate_lag = calc_lag(open_date, estimate_date)
        open_to_1st_pay_lag = calc_lag(open_date, first_payment_date)
        open_to_subro_lag = calc_lag(open_date, subrogation_date)
        open_to_closed_lag = calc_lag(open_date, close_date)

        data.append({
            'claim_open_date_id': format_date(open_date),
            'claim_accident_date_id': format_date(accident_date),
            'claim_estimate_date_id': format_date(estimate_date),
            'claim_1st_payment_date_id': format_date(first_payment_date),
            'claim_most_recent_payment_date_id': format_date(most_recent_payment_date),
            'claim_subrogation_date_id': format_date(subrogation_date),
            'claim_close_date_id': format_date(close_date),
            'policyholder_id': random.randint(1000, 9999),
            'claim_supervisor_id': random.randint(10, 99),
            'agent_id': random.randint(100, 999),
            'coverage_id': random.randint(1, 20),
            'covered_item_id': random.randint(10000, 99999),
            'claimant_id': random.randint(1000, 9999),
            'claim_status_id': 1 if is_closed else 2,
            'claim_profile_id': random.randint(1, 5),
            'claim_id': i + 1,
            'policy_number': f"POL-{random.randint(10000, 99999)}",
            'original_reserve_nok_amount': original_reserve,
            'estimate_nok_amount': estimate_nok,
            'current_reserve_to_date_nok_amount': current_reserve,
            'claim_paid_to_date_nok_amount': paid_to_date,
            'salvage_collected_to_date_nok_amount': salvage_collected,
            'subro_payment_collected_to_date_nok_amount': subro_collected,
            'claim_accident_to_open_lag': accident_to_open_lag,
            'claim_open_to_estimate_lag': open_to_estimate_lag,
            'claim_open_to_1st_payment_lag': open_to_1st_pay_lag,
            'claim_open_to_subrogation_lag': open_to_subro_lag,
            'claim_open_to_closed_lag': open_to_closed_lag,
            'number_of_claim_transactions': random.randint(1, 15)
        })

    df = pd.DataFrame(data)
    
    # Determine the output directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'data', 'raw', 'claim_accumulated_snapshot'))
    
    os.makedirs(out_dir, exist_ok=True)
    df.to_parquet(os.path.join(out_dir, 'claim_accumulating_snapshot.parquet'), index=False)
    print(f"Parquet generated successfully with {num_rows} rows in {out_dir}")

if __name__ == "__main__":
    generate_mock_data()
