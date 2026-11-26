import streamlit as st
import pandas as pd
from engine import generate,lifecycle,cohorts
st.set_page_config(page_title="Customer Journey",layout="wide")
st.caption("ANALYTICS INTELLIGENCE LAB / PORTFOLIO / V2.0")
st.title("Customer Journey | Lifecycle intelligence")
st.caption("Synthetic events · inactivity is a churn proxy, not a confirmed cancellation")
volume=st.sidebar.selectbox("Synthetic customers",[1500,3000,5000])
@st.cache_data
def demo(n):
    return generate(n)
df=demo(volume)
cutoff=st.sidebar.date_input("Observation cutoff",pd.Timestamp("2025-12-31").date(),min_value=pd.Timestamp("2025-01-01").date(),max_value=pd.Timestamp("2025-12-31").date())
risk=st.sidebar.slider("Risk days",15,90,60)
churn=st.sidebar.slider("Churn proxy days",risk+1,180,120)
states=lifecycle(df,cutoff,risk,churn)
matrix=cohorts(df,cutoff)
for c,(label,val) in zip(st.columns(3),[("Customers",len(states)),("At risk",states.state.eq("At risk").sum()),("Churn proxy",states.state.eq("Churn proxy").sum())]): c.metric(label,int(val))
st.subheader("Lifecycle distribution")
st.bar_chart(states.state.value_counts(), color="#2563EB")
st.subheader("Inactivity distribution")
st.bar_chart(pd.cut(states.idle_days,[-1,30,60,90,120,1000]).value_counts(sort=False).rename(index=str), color="#0F766E")
st.subheader("Monthly activity retention")
st.dataframe(matrix.style.format("{:.0%}",na_rep="—").map(lambda v: "" if pd.isna(v) else f"background-color: rgba(37,99,235,{0.12+0.45*v})"))
st.caption("M0 includes acquisition. Later months measure observed activity; future periods are blank. Current month may be partial.")
st.subheader("Customer explorer")
selected=st.multiselect("Lifecycle states", sorted(states.state.unique()), default=sorted(states.state.unique()))
st.dataframe(states[states.state.isin(selected)])
st.download_button("Export lifecycle",states.to_csv(index=False),"lifecycle.csv")
st.download_button("Export cohorts",matrix.to_csv(),"cohorts.csv")


st.divider()
st.caption("Rodrigo Alcantara | Analytics Intelligence Lab | Synthetic demonstration")
