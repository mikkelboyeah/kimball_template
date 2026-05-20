with source as (
    select * from {{ source('raw', 'fact_premium_periodic_snapshot') }}
),

renamed as (
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
    from source
)

select * from renamed
