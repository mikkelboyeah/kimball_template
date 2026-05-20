with source as (
    select * from {{ source('raw', 'dim_policy_status') }}
),

renamed as (
    select
        policy_status_id,
        status_name,
        status_description
    from source
)

select * from renamed
