#!/usr/bin/env python3
from pathlib import Path
import sys, pandas as pd
O = Path(__file__).resolve().parents[1] / "data" / "sample"
e=[]
a=pd.read_csv(O/"fact_actuals.csv"); j=pd.read_csv(O/"dim_job.csv")
if a["ActualKey"].duplicated().any(): e.append("dup ActualKey")
if not set(a.JobKey).issubset(set(j.JobKey)): e.append("orphan JobKey actuals")
if len(a)<25000: e.append(f"actuals too small {len(a)}")
if e:
    print("FAIL"); [print("-",x) for x in e]; sys.exit(1)
print(f"OK actuals={len(a):,} labour={len(pd.read_csv(O/'fact_labour.csv')):,} wip={len(pd.read_csv(O/'fact_wip.csv')):,}")
