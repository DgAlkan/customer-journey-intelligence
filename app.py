import streamlit as st
import pandas as pd
from engine import generate,lifecycle,cohorts
st.set_page_config(page_title="Customer Journey",layout="wide")
st.caption("ANALYTICS INTELLIGENCE LAB | Independent portfolio project")
st.title("Customer Journey | Lifecycle intelligence")
st.caption("Synthetic events · inactivity is a churn proxy, not a confirmed cancellation")
df=generate()
cutoff=st.sidebar.date_input("Observation cutoff",pd.Timestamp("2025-12-31").date(),min_value=pd.Timestamp("2025-01-01").date(),max_value=pd.Timestamp("2025-12-31").date())
risk=st.sidebar.slider("Risk days",15,90,60)
churn=st.sidebar.slider("Churn proxy days",risk+1,180,120)
states=lifecycle(df,cutoff,risk,churn)
matrix=cohorts(df,cutoff)
for c,(label,val) in zip(st.columns(3),[("Customers",len(states)),("At risk",states.state.eq("At risk").sum()),("Churn proxy",states.state.eq("Churn proxy").sum())]): c.metric(label,int(val))
st.bar_chart(states.state.value_counts())
st.subheader("Monthly activity retention")
st.dataframe(matrix.style.format("{:.0%}",na_rep="—"))
st.caption("M0 includes acquisition. Later months measure observed activity; future periods are blank. Current month may be partial.")
st.dataframe(states)
st.download_button("Export lifecycle",states.to_csv(index=False),"lifecycle.csv")
st.download_button("Export cohorts",matrix.to_csv(),"cohorts.csv")


st.divider()
st.caption("Rodrigo Alcantara | Analytics Intelligence Lab | Synthetic demonstration")
