/*
Consolidated Periodic Snapshot
Grain: One row per month per policyholder, covered_item, coverage, agent.
Includes metrics from both Premium and Claim snapshots.
*/

with premium as (
    select
        month_end_snapshot_date_id,
        policyholder_id,
        agent_id,
        coverage_id,
        covered_item_id,
        policy_number,
        policy_status_id,
        sum(written_premium_revenue_amount) as written_premium_revenue_dollar_amount,
        sum(earned_premium_revenue_amount) as earned_premium_revenue_dollar_amount
    from {{ ref('stg_prem_ps__fact_premium_periodic_snapshot') }}
    group by 1, 2, 3, 4, 5, 6, 7
),

claims as (
    select
        month_end_snapshot_date_id,
        policyholder_id,
        agent_id,
        coverage_id,
        covered_item_id,
        policy_number,
        claim_status_id,
        sum(amount_paid) as claim_paid_dollar_amount,
        sum(amount_claimed) as claim_total_claimed_dollar_amount
    from {{ ref('stg_clm_ps__fact_claim_periodic_snapshot') }}
    group by 1, 2, 3, 4, 5, 6, 7
),

joined as (
    select
        coalesce(p.month_end_snapshot_date_id, c.month_end_snapshot_date_id) as month_end_snapshot_date_id,
        coalesce(p.policyholder_id, c.policyholder_id) as policyholder_id,
        coalesce(p.agent_id, c.agent_id) as agent_id,
        coalesce(p.coverage_id, c.coverage_id) as coverage_id,
        coalesce(p.covered_item_id, c.covered_item_id) as covered_item_id,
        coalesce(p.policy_number, c.policy_number) as policy_number,
        p.policy_status_id,
        c.claim_status_id,
        coalesce(p.written_premium_revenue_dollar_amount, 0) as written_premium_revenue_dollar_amount,
        coalesce(p.earned_premium_revenue_dollar_amount, 0) as earned_premium_revenue_dollar_amount,
        coalesce(c.claim_paid_dollar_amount, 0) as claim_paid_dollar_amount,
        coalesce(c.claim_total_claimed_dollar_amount, 0) as claim_total_claimed_dollar_amount
    from premium p
    full outer join claims c
        on p.month_end_snapshot_date_id = c.month_end_snapshot_date_id
        and p.policyholder_id = c.policyholder_id
        and p.agent_id = c.agent_id
        and p.coverage_id = c.coverage_id
        and p.covered_item_id = c.covered_item_id
        and p.policy_number = c.policy_number
)

select * from joined
