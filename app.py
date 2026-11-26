import streamlit as st
import pandas as pd
from engine import generate,lifecycle,cohorts
st.set_page_config(page_title="Customer Journey",layout="wide")
st.markdown("""<style>
.stApp {background:#f1f5f9;}
[data-testid="stSidebar"] {background:#142238;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] h2 {color:#e2e8f0;}
[data-testid="stMetric"] {background:white;border:1px solid #dbe4ef;border-radius:14px;padding:16px;box-shadow:0 3px 12px #10223808;}
[data-testid="stMetricValue"] {font-weight:700;color:#102238;}
[data-testid="stMainBlockContainer"] {padding-top:2rem;max-width:1440px;}
.stTabs [role="tablist"] {gap:12px;}
.stTabs [role="tab"] {font-weight:600;}
.lab-hero {background:linear-gradient(115deg,#0b1526,#193a60);color:white;padding:28px 30px;border-radius:16px;margin-bottom:18px;}
.lab-hero h1 {color:white;font-size:clamp(1.65rem,3vw,2.5rem);margin:8px 0;padding:0;}
.lab-hero p {color:#cbd5e1;margin:0;}
.lab-kicker {color:#7dd3fc;font-size:12px;font-weight:700;letter-spacing:1.8px;}
</style>
<section class="lab-hero"><div class="lab-kicker">ANALYTICS INTELLIGENCE LAB</div><h1>Customer Journey Intelligence</h1><p>Lifecycle · Engagement · Retention</p></section>""", unsafe_allow_html=True)
st.sidebar.header("Workspace")
st.sidebar.caption("Configure your synthetic demonstration.")
st.sidebar.markdown("### Product suite")
st.sidebar.markdown("[01 · Data Quality](https://dgalkan-data-quality.streamlit.app)  \n[02 · Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app)  \n[03 · Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
st.sidebar.divider()
st.sidebar.markdown("### Analysis controls")
with st.expander("About this product · methodology"):
    st.markdown("Explore engagement, inactivity and monthly activity cohorts.")
    st.markdown("Lifecycle states use configurable inactivity thresholds. Cohorts measure observed monthly activity; churn is a proxy and the current month may be incomplete.")
    st.markdown("[Technical portfolio](https://github.com/DgAlkan) · Synthetic data only.")
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
if len(states):
    st.info(f"{states.state.isin(['At risk', 'Churn proxy']).mean():.1%} of observed customers are classified as at risk or churn proxy under the selected thresholds.")
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
st.caption("Rodrigo Alcantara | Analytics Intelligence Lab | Independent synthetic demonstration")
st.markdown("[Data Quality](https://dgalkan-data-quality.streamlit.app) · [Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app) · [Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
