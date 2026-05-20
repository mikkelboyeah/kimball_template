-- The number of claims in the consolidated snapshot should match the number of claims in the claim snapshot.
-- This test fails if the counts are unequal.
WITH consolidated_claims AS (
    SELECT count(*) as claim_count
    FROM {{ ref('fact_insurance_consolidated_snapshot') }}
    WHERE (claim_paid_dollar_amount > 0 OR claim_total_claimed_dollar_amount > 0)
),
raw_claims AS (
    SELECT count(*) as claim_count
    FROM {{ ref('fact_claim_periodic_snapshot') }}
    WHERE (amount_paid > 0 OR amount_claimed > 0)
)
SELECT *
FROM (
    SELECT (SELECT claim_count FROM consolidated_claims) != (SELECT claim_count FROM raw_claims) as is_mismatch
)
WHERE is_mismatch = true
