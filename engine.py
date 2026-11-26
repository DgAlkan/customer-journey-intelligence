import pandas as pd
import numpy as np

def generate(n=1500, seed=42):
    rng=np.random.default_rng(seed)
    rows=[]
    for i in range(n):
        start=pd.Timestamp("2025-01-01")+pd.Timedelta(days=int(rng.integers(0,270)))
        rows.append((i,start,"acquisition"))
        for offset in range(1,12):
            date=start+pd.Timedelta(days=30*offset)
            if date<=pd.Timestamp("2025-12-31") and rng.random()<.85**offset:
                rows.append((i,date,"engagement"))
    return pd.DataFrame(rows,columns=["customer_id","date","event"])

def prepare(df, cutoff):
    x=df.copy()
    x["date"]=pd.to_datetime(x.date,errors="raise")
    if x[["customer_id","date","event"]].isna().any().any() or x.duplicated().any(): raise ValueError("Invalid or duplicate event")
    if not x.event.isin(["acquisition","engagement"]).all(): raise ValueError("Invalid event")
    x=x[x.date<=pd.Timestamp(cutoff)].copy()
    return x

def lifecycle(df, cutoff, risk=60, churn=120):
    if not 0<risk<churn: raise ValueError("Invalid thresholds")
    x=prepare(df,cutoff)
    rows=[]
    for k,g in x.groupby("customer_id"):
        dates=g.loc[g.event.eq("engagement"),"date"].sort_values()
        age=(pd.Timestamp(cutoff)-g.date.min()).days
        idle=(pd.Timestamp(cutoff)-(dates.max() if len(dates) else g.date.min())).days
        gap=dates.diff().dt.days.iloc[-1] if len(dates)>1 else 0
        state="Churn proxy" if idle>=churn else "At risk" if idle>=risk else "Acquired" if not len(dates) else "Reactivated" if gap>=churn else "Engaged"
        rows.append((k,age,idle,len(dates),state))
    return pd.DataFrame(rows,columns=["customer_id","age_days","idle_days","engagements","state"])

def cohorts(df, cutoff):
    x=prepare(df,cutoff)
    x["month"]=x.date.dt.to_period("M")
    x["cohort"]=x.groupby("customer_id").month.transform("min")
    x["offset"]=(x.month.astype("int64")-x.cohort.astype("int64"))
    sizes=x.groupby("cohort").customer_id.nunique()
    counts=x.groupby(["cohort","offset"]).customer_id.nunique().unstack()
    end=pd.Timestamp(cutoff).to_period("M")
    result=counts.reindex(columns=range(int((end-min(sizes.index)).n)+1)).div(sizes,axis=0) if len(sizes) else counts
    for c in result.index:
        for m in result.columns:
            result.loc[c,m]=float("nan") if c+m>end else (0 if pd.isna(result.loc[c,m]) else result.loc[c,m])
    result.index=result.index.astype(str)
    return result
