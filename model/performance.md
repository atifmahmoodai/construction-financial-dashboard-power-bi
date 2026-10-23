# Performance

- Import mode for sample and most mid-market job-cost extracts from QBO/Excel
- Aggregate actuals to Job × CostCode × Month for executive page
- WIP is monthly snapshot — do not sum PercentComplete across jobs without weighting
- Decision: DirectQuery only if live ERP; otherwise nightly Import
