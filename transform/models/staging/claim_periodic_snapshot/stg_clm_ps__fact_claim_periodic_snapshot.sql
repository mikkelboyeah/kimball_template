with source as (
    select * from {{ source('raw', 'fact_claim_periodic_snapshot') }}
),

renamed as (
    select
        claim_id,
        policyholder_id,
        claim_supervisor_id,
        agent_id,
        coverage_id,
        covered_item_id,
        claimant_id,
        claim_status_id,
        claim_profile_id,
        policy_number,
        claim_number,
        month_end_snapshot_date_id,
        amount_claimed,
        amount_paid,
        change_in_reserve,
        current_reserve_balance
    from source
)

select * from renamed
