with source as (
    select * from {{ source('raw', 'factless_accident_events') }}
),

renamed as (
    select
        claim_loss_date_id,
        policyholder_id,
        coverage_id,
        covered_item_id,
        claimant_id,
        loss_party_id,
        loss_party_role_id,
        claim_profile_id,
        claim_number as claim_number_dd,
        policy_number as policy_number_dd,
        accident_involvement_count
    from source
)

select * from renamed
