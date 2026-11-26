import pandas as pd
import pytest
from engine import generate,lifecycle,cohorts
def fixture():
    return pd.DataFrame({"customer_id":[1,1,2],"date":["2025-01-01","2025-03-01","2025-01-02"],"event":["acquisition","engagement","acquisition"]})
def test_cohort():
    m=cohorts(fixture(),"2025-03-31")
    assert m.loc["2025-01",0]==1
    assert m.loc["2025-01",1]==0
    assert m.loc["2025-01",2]==.5
def test_cutoff():
    assert lifecycle(fixture(),"2025-02-01").engagements.sum()==0
def test_churn():
    assert lifecycle(fixture(),"2025-12-31").state.eq("Churn proxy").all()
def test_duplicate():
    with pytest.raises(ValueError): lifecycle(pd.concat([fixture(),fixture()]),"2025-12-31")
def test_seed():
    assert generate(20).equals(generate(20))
