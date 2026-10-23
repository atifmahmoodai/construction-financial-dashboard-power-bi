#!/usr/bin/env python3
"""Production-scale construction financial sample data (multi-entity CAD/USD)."""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample"
SEED = 7
START = date(2023, 1, 1)
END = date(2026, 9, 30)


def date_key(d: date) -> int:
    return int(d.strftime("%Y%m%d"))


def build_dim_date(start: date, end: date) -> pd.DataFrame:
    rows = []
    d = start
    while d <= end:
        rows.append(
            {
                "DateKey": date_key(d),
                "Date": d.isoformat(),
                "Year": d.year,
                "Quarter": f"Q{(d.month - 1) // 3 + 1}",
                "MonthNumber": d.month,
                "MonthName": d.strftime("%B"),
                "MonthShort": d.strftime("%b"),
                "FiscalYear": d.year if d.month >= 4 else d.year - 1,
            }
        )
        d += timedelta(days=1)
    return pd.DataFrame(rows)


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    entities = pd.DataFrame(
        [
            {"EntityKey": 1, "EntityId": "ENT-CA-ON", "EntityName": "NorthPeak Construction Ltd", "CurrencyCode": "CAD", "Country": "CA", "GSTRate": 0.05, "PSTRate": 0.08},
            {"EntityKey": 2, "EntityId": "ENT-US-TX", "EntityName": "NorthPeak US LLC", "CurrencyCode": "USD", "Country": "US", "GSTRate": 0.0, "PSTRate": 0.0},
            {"EntityKey": 3, "EntityId": "ENT-CA-BC", "EntityName": "Pacific Build Group", "CurrencyCode": "CAD", "Country": "CA", "GSTRate": 0.05, "PSTRate": 0.07},
        ]
    )

    cost_codes = []
    families = [
        ("01", "General Conditions"),
        ("03", "Concrete"),
        ("05", "Metals"),
        ("06", "Wood & Plastics"),
        ("07", "Thermal & Moisture"),
        ("09", "Finishes"),
        ("15", "Mechanical"),
        ("16", "Electrical"),
        ("26", "Electrical Power"),
        ("31", "Earthwork"),
        ("32", "Exterior Improvements"),
        ("33", "Utilities"),
    ]
    ck = 1
    for fam, fname in families:
        for j in range(1, 5):
            cost_codes.append(
                {
                    "CostCodeKey": ck,
                    "CostCode": f"{fam}-{j:02d}",
                    "CostCodeName": f"{fname} - Item {j}",
                    "CostFamily": fname,
                    "CostType": ["Labour", "Material", "Subcontract", "Equipment"][j % 4],
                }
            )
            ck += 1
    dim_cost_code = pd.DataFrame(cost_codes)

    statuses = ["Active", "Active", "Active", "Complete", "Warranty", "On Hold"]
    job_types = ["Commercial", "Industrial", "Institutional", "Residential Multi", "Infrastructure"]
    jobs = []
    for i in range(1, 61):
        ent = int(rng.integers(1, 4))
        start = START + timedelta(days=int(rng.integers(0, 700)))
        dur = int(rng.integers(180, 750))
        end_j = start + timedelta(days=dur)
        contract = float(rng.uniform(0.8e6, 28e6))
        jobs.append(
            {
                "JobKey": i,
                "JobId": f"JOB-{i:04d}",
                "JobName": f"Project {i:04d}",
                "EntityKey": ent,
                "JobType": job_types[i % len(job_types)],
                "Status": statuses[i % len(statuses)],
                "ContractValue": round(contract, 2),
                "StartDate": start.isoformat(),
                "EndDatePlanned": end_j.isoformat(),
                "PMName": f"PM {(i % 12) + 1}",
                "ClientName": f"Owner {(i % 20) + 1}",
            }
        )
    dim_job = pd.DataFrame(jobs)

    # Budget versions
    budget_rows = []
    bk = 1
    for _, job in dim_job.iterrows():
        versions = ["Baseline", "Current"]
        if rng.random() < 0.4:
            versions.append("Forecast")
        for ver in versions:
            scale = 1.0 if ver == "Baseline" else float(rng.uniform(0.95, 1.12))
            for _, cc in dim_cost_code.sample(n=int(rng.integers(18, 36)), random_state=int(job.JobKey)).iterrows():
                amt = round(float(job.ContractValue) * float(rng.uniform(0.004, 0.045)) * scale, 2)
                budget_rows.append(
                    {
                        "BudgetKey": bk,
                        "JobKey": int(job.JobKey),
                        "CostCodeKey": int(cc.CostCodeKey),
                        "BudgetVersion": ver,
                        "BudgetAmount": amt,
                        "AsOfDateKey": date_key(date(2026, 6, 30) if ver != "Baseline" else date.fromisoformat(job.StartDate)),
                    }
                )
                bk += 1
    fact_budget = pd.DataFrame(budget_rows)

    # Actuals — large
    actual_rows = []
    ak = 1
    n_actuals = 45_000
    job_keys = dim_job["JobKey"].to_numpy()
    jw = np.array([float(dim_job.loc[dim_job.JobKey == j, "ContractValue"].iloc[0]) for j in job_keys])
    jw /= jw.sum()
    cc_keys = dim_cost_code["CostCodeKey"].to_numpy()
    span = (END - START).days
    for i in range(n_actuals):
        jk = int(rng.choice(job_keys, p=jw))
        job = dim_job.loc[dim_job.JobKey == jk].iloc[0]
        d = START + timedelta(days=int(rng.integers(0, span)))
        # keep actuals roughly within job window when possible
        js = date.fromisoformat(job.StartDate)
        if d < js:
            d = js + timedelta(days=int(rng.integers(0, 30)))
        amt = round(float(rng.lognormal(8.5, 1.1)), 2)
        actual_rows.append(
            {
                "ActualKey": ak,
                "JobKey": jk,
                "CostCodeKey": int(rng.choice(cc_keys)),
                "TxnDateKey": date_key(d),
                "TxnDate": d.isoformat(),
                "SourceSystem": rng.choice(["QBO", "QBO", "Payroll", "AP", "JobCost"]),
                "ActualAmount": amt,
                "Qty": round(float(rng.uniform(1, 120)), 2) if rng.random() < 0.4 else None,
                "VendorName": f"Vendor {int(rng.integers(1, 90))}",
                "IsCommitted": 1 if rng.random() < 0.15 else 0,
            }
        )
        ak += 1
    fact_actuals = pd.DataFrame(actual_rows)

    # Change orders
    co_rows = []
    cok = 1
    for _, job in dim_job.iterrows():
        for _ in range(int(rng.integers(0, 8))):
            d = date.fromisoformat(job.StartDate) + timedelta(days=int(rng.integers(30, 400)))
            if d > END:
                d = END - timedelta(days=int(rng.integers(0, 60)))
            amt = round(float(rng.uniform(-25000, 350000)), 2)
            co_rows.append(
                {
                    "ChangeOrderKey": cok,
                    "JobKey": int(job.JobKey),
                    "ChangeOrderId": f"CO-{job.JobId}-{cok}",
                    "ApprovedDateKey": date_key(d),
                    "Status": rng.choice(["Approved", "Approved", "Pending", "Rejected"]),
                    "Amount": amt,
                    "Description": rng.choice(["Scope add", "Owner request", "Field condition", "Credit", "Allowance"]),
                }
            )
            cok += 1
    fact_change_orders = pd.DataFrame(co_rows)

    # Labour
    labour_rows = []
    lk = 1
    for i in range(28_000):
        jk = int(rng.choice(job_keys, p=jw))
        d = START + timedelta(days=int(rng.integers(0, span)))
        hours = round(float(rng.choice([4, 8, 8, 8, 10, 12])), 1)
        rate = float(rng.uniform(28, 95))
        labour_rows.append(
            {
                "LabourKey": lk,
                "JobKey": jk,
                "CostCodeKey": int(rng.choice(cc_keys)),
                "WorkDateKey": date_key(d),
                "WorkDate": d.isoformat(),
                "EmployeeId": f"EMP-{int(rng.integers(1, 180)):04d}",
                "Craft": rng.choice(["Carpenter", "Electrician", "Labourer", "Operator", "Plumber", "Ironworker"]),
                "Hours": hours,
                "BurdenedRate": round(rate, 2),
                "LabourCost": round(hours * rate, 2),
                "IsOvertime": 1 if hours > 8 else 0,
            }
        )
        lk += 1
    fact_labour = pd.DataFrame(labour_rows)

    # AR aging snapshot
    ar_rows = []
    ark = 1
    for _, job in dim_job.iterrows():
        if job.Status == "On Hold":
            continue
        for bucket in ["Current", "1-30", "31-60", "61-90", "90+"]:
            if rng.random() < 0.35 and bucket != "Current":
                continue
            bal = round(float(rng.uniform(5_000, 450_000)) * (1.6 if bucket == "Current" else 0.7), 2)
            ar_rows.append(
                {
                    "ARKey": ark,
                    "JobKey": int(job.JobKey),
                    "EntityKey": int(job.EntityKey),
                    "AsOfDateKey": date_key(END),
                    "AgingBucket": bucket,
                    "BucketSort": {"Current": 1, "1-30": 2, "31-60": 3, "61-90": 4, "90+": 5}[bucket],
                    "OpenBalance": bal,
                    "InvoiceCount": int(rng.integers(1, 12)),
                }
            )
            ark += 1
    fact_ar_aging = pd.DataFrame(ar_rows)

    # WIP monthly by job (over/under billing)
    wip_rows = []
    wk = 1
    months = pd.date_range("2024-01-01", END.isoformat(), freq="MS")
    for _, job in dim_job.iterrows():
        contract = float(job.ContractValue)
        # approved COs
        cos = fact_change_orders[
            (fact_change_orders.JobKey == job.JobKey) & (fact_change_orders.Status == "Approved")
        ]["Amount"].sum()
        revised = contract + float(cos)
        cost_to_date = 0.0
        billed_to_date = 0.0
        for m in months:
            if m.date() < date.fromisoformat(job.StartDate):
                continue
            cost_to_date += float(rng.uniform(0.01, 0.06)) * revised
            pct_complete = min(0.99, cost_to_date / max(revised * 0.85, 1))
            earned = revised * pct_complete
            billed_to_date += float(rng.uniform(0.02, 0.07)) * revised
            over_under = billed_to_date - earned
            wip_rows.append(
                {
                    "WipKey": wk,
                    "JobKey": int(job.JobKey),
                    "PeriodDateKey": date_key(m.date()),
                    "PeriodMonth": m.strftime("%Y-%m"),
                    "RevisedContract": round(revised, 2),
                    "CostToDate": round(cost_to_date, 2),
                    "PercentComplete": round(pct_complete, 4),
                    "EarnedRevenue": round(earned, 2),
                    "BilledToDate": round(billed_to_date, 2),
                    "OverUnderBilling": round(over_under, 2),
                    "EstimatedCostAtCompletion": round(revised * float(rng.uniform(0.82, 0.98)), 2),
                    "EstimatedProfit": round(revised - revised * float(rng.uniform(0.82, 0.98)), 2),
                }
            )
            wk += 1
            if pct_complete > 0.97:
                break
    fact_wip = pd.DataFrame(wip_rows)

    dim_date = build_dim_date(START, END)
    dim_date.to_csv(OUT / "dim_date.csv", index=False)
    entities.to_csv(OUT / "dim_entity.csv", index=False)
    dim_job.to_csv(OUT / "dim_job.csv", index=False)
    dim_cost_code.to_csv(OUT / "dim_cost_code.csv", index=False)
    fact_budget.to_csv(OUT / "fact_budget.csv", index=False)
    fact_actuals.to_csv(OUT / "fact_actuals.csv", index=False)
    fact_change_orders.to_csv(OUT / "fact_change_orders.csv", index=False)
    fact_labour.to_csv(OUT / "fact_labour.csv", index=False)
    fact_ar_aging.to_csv(OUT / "fact_ar_aging.csv", index=False)
    fact_wip.to_csv(OUT / "fact_wip.csv", index=False)

    for p in sorted(OUT.glob("*.csv")):
        print(f"{p.name}: {sum(1 for _ in open(p)) - 1:,}")


if __name__ == "__main__":
    main()
