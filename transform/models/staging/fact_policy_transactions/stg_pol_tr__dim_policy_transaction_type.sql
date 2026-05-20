with source as (
    select * from {{ source('raw', 'dim_policy_transaction_type') }}
),

renamed as (
    select
        policy_transaction_type_id,
        transaction_category,
        transaction_reason_description
    from source
)

select * from renamed
