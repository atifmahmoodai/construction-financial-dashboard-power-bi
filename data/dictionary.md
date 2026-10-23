# Data dictionary — construction financials

Multi-entity sample (CAD + USD). Tax rates on `dim_entity` support GST/PST notes for Canadian entities; amounts are stored in **entity local currency** unless noted.

| Table | Grain | Rows | PII |
|-------|-------|------|-----|
| dim_date | Day | ~1.4k | None |
| dim_entity | Legal entity | 3 | Fake company names |
| dim_job | Job / project | 60 | Fake PM/client names |
| dim_cost_code | Cost code | 48 | None |
| fact_budget | Job × cost code × budget version | ~3.8k | None |
| fact_actuals | Cost transaction | **45,000** | Vendor names (fake) |
| fact_labour | Labour punch | **28,000** | EmployeeId surrogate |
| fact_change_orders | CO header | ~200 | None |
| fact_wip | Job × month WIP | ~1.4k | None |
| fact_ar_aging | Job × aging bucket snapshot | ~185 | None |

## WIP / over-under billing
`OverUnderBilling = BilledToDate − EarnedRevenue` where `EarnedRevenue = RevisedContract × PercentComplete`. Positive = overbilling; negative = underbilling.
