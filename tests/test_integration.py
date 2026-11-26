import pandas as pd
import duckdb
from streamlit.testing.v1 import AppTest
from engine import generate, lifecycle, cohorts

def test_sql(tmp_path,monkeypatch):
    from pathlib import Path
    sql=Path("sql/analysis.sql").read_text()
    monkeypatch.chdir(tmp_path)
    Path("data").mkdir()
    x=generate(100)
    x.to_csv("data/synthetic.csv",index=False)
    m=cohorts(x,"2025-12-31")
    with duckdb.connect() as con:
        rows=con.execute(sql).fetchall()
    for c,k,v in rows:
        assert abs(m.loc[pd.Timestamp(c).strftime("%Y-%m"),k]-v)<1e-9

def test_boundaries():
    x=pd.DataFrame({"customer_id":[1],"date":["2025-01-01"],"event":["acquisition"]})
    assert lifecycle(x,"2025-03-02").state.iloc[0]=="At risk"
    assert lifecycle(x,"2025-05-01").state.iloc[0]=="Churn proxy"

def test_app():
    a=AppTest.from_file("app.py",default_timeout=60).run()
    assert not a.exception
    assert len(a.metric)==3
