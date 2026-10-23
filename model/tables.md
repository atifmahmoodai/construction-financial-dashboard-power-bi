# Tables & hierarchies

- dim_date — Date table; hierarchy Year → Quarter → Month
- dim_entity — CurrencyCode, GSTRate, PSTRate
- dim_job — hierarchy EntityName (via rel) → JobType → JobName; Status
- dim_cost_code — hierarchy CostFamily → CostCode
- fact_budget, fact_actuals, fact_labour, fact_change_orders, fact_wip, fact_ar_aging

## Sort-by
- MonthName ← MonthNumber; AgingBucket ← BucketSort; BudgetVersion custom sort Baseline=1, Current=2, Forecast=3

## Display folders
Core Finance | WIP | Labour | AR & Cash | Time Intelligence | Tax Helpers
