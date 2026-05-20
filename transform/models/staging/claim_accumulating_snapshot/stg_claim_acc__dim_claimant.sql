select * from {{ source('raw', 'dim_claimant') }}
