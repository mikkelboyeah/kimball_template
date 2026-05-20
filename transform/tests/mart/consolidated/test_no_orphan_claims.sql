-- Every claim in the consolidated snapshot should have some premium data associated with it.
-- This test fails if it returns rows where there is claim activity but no premium data.
SELECT *
FROM {{ ref('fact_insurance_consolidated_snapshot') }}
WHERE (claim_paid_dollar_amount > 0 OR claim_total_claimed_dollar_amount > 0)
  AND (written_premium_revenue_dollar_amount = 0 AND earned_premium_revenue_dollar_amount = 0)
