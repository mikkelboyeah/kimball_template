select
    month_end_snapshot_date_id,
    policyholder_id,
    agent_id,
    coverage_id,
    covered_item_id,
    policy_number,
    policy_status_id,
    written_premium_revenue_amount,
    earned_premium_revenue_amount
from {{ ref('stg_prem_ps__fact_premium_periodic_snapshot') }}
