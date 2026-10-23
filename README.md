# Power BI — Construction financial & WIP dashboard

Finance-grade job cost, WIP (over/under billing), AR aging, and labour analytics for GCs — packaged as sellable delivery IP (indicative **$2.5k–$20k** engagements).

```mermaid
flowchart LR
  QBO[QBO / Excel / JobCost] --> PQ[Power Query]
  PQ --> M[Star schema]
  M --> P[Exec / Job / WIP / AR / Labour]
```

## Quick start
```bash
pip install -r requirements.txt
python scripts/generate_sample_data.py
python scripts/validate_schema.py
```
Build PBIX from `model/`, `dax/`, `report/pages/`, apply `report/theme.json`.

## Scale (v2)
fact_actuals **45,000** · fact_labour **28,000** · fact_wip ~1,400 · fact_budget ~3,800

## Licence
MIT — see `LICENSE`.
