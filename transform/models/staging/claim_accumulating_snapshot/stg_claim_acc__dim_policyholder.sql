select * from {{ source('raw', 'dim_policyholder') }}
