import streamlit as st
import pandas as pd
from engine import generate,lifecycle,cohorts
st.set_page_config(page_title="Customer Journey",layout="wide")
lang = st.sidebar.radio("Idioma / Language", ["Português", "English"], horizontal=True, key="lab_language")
def tr(en, pt):
    return pt if lang == "Português" else en
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
<section class="lab-hero"><div class="lab-kicker">ANALYTICS INTELLIGENCE LAB</div><h1>Customer Journey Intelligence</h1><p>__LAB_SUBTITLE__</p></section>""".replace("__LAB_SUBTITLE__", tr("Lifecycle · Engagement · Retention", "Ciclo de vida · Engajamento · Retenção")), unsafe_allow_html=True)
st.sidebar.header(tr("Workspace", "Área de trabalho"))
st.sidebar.caption(tr("Configure your synthetic demonstration.", "Configure sua demonstração com dados sintéticos."))
st.sidebar.markdown(tr("### Product suite", "### Produtos"))
st.sidebar.markdown("[01 · Data Quality](https://dgalkan-data-quality.streamlit.app)  \n[02 · Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app)  \n[03 · Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
st.sidebar.divider()
st.sidebar.markdown(tr("### Analysis controls", "### Filtros e parâmetros"))
with st.expander(tr("About this product · methodology", "Sobre o produto · metodologia")):
    st.markdown(tr("Explore engagement, inactivity and monthly activity cohorts.", "Explore engajamento, inatividade e coortes de atividade mensal."))
    st.markdown(tr("Lifecycle states use configurable inactivity thresholds. Cohorts measure observed monthly activity; churn is a proxy and the current month may be incomplete.", "As classificações usam limites configuráveis de inatividade. As coortes medem atividade mensal observada; churn é uma aproximação e o mês atual pode estar incompleto."))
    st.markdown(tr("[Technical portfolio](https://github.com/DgAlkan) · Synthetic data only.", "[Portfólio técnico](https://github.com/DgAlkan) · Apenas dados sintéticos."))
st.caption(tr("Synthetic events · inactivity is a churn proxy, not a confirmed cancellation", "Eventos sintéticos · inatividade indica churn potencial, não cancelamento confirmado"))
volume=st.sidebar.selectbox(tr("Synthetic customers", "Clientes sintéticos"),[1500,3000,5000])
@st.cache_data
def demo(n):
    return generate(n)
df=demo(volume)
cutoff=st.sidebar.date_input(tr("Observation cutoff", "Data de corte"),pd.Timestamp("2025-12-31").date(),min_value=pd.Timestamp("2025-01-01").date(),max_value=pd.Timestamp("2025-12-31").date())
risk=st.sidebar.slider(tr("Risk days", "Dias para risco"),15,90,60)
churn=st.sidebar.slider(tr("Churn proxy days", "Dias para churn potencial"),risk+1,180,120)
states=lifecycle(df,cutoff,risk,churn)
matrix=cohorts(df,cutoff)
for c,(label,val) in zip(st.columns(3),[(tr("Customers", "Clientes"),len(states)),("At risk",states.state.eq("At risk").sum()),("Churn proxy",states.state.eq("Churn proxy").sum())]): c.metric(tr(label, {"Clientes":"Clientes","Customers":"Clientes","At risk":"Em risco","Churn proxy":"Churn potencial"}[label]),int(val))
st.subheader(tr("Lifecycle distribution", "Distribuição do ciclo de vida"))
if len(states):
    share = states.state.isin(["At risk", "Churn proxy"]).mean()
    st.info(tr(f"{share:.1%} of observed customers are classified as at risk or churn proxy under the selected thresholds.", f"{share:.1%} dos clientes observados estão em risco ou churn potencial, conforme os limites selecionados."))
state_pt = {"At risk":"Em risco","Churn proxy":"Churn potencial","Acquired":"Adquirido","Engaged":"Engajado","Reactivated":"Reativado"}
st.bar_chart(states.state.value_counts().rename(index=lambda x: tr(x,state_pt.get(x,x))), color="#2563EB")
st.subheader(tr("Inactivity distribution", "Distribuição da inatividade"))
st.bar_chart(pd.cut(states.idle_days,[-1,30,60,90,120,1000]).value_counts(sort=False).rename(index=str), color="#0F766E")
st.subheader(tr("Monthly activity retention", "Retenção mensal por coorte"))
st.dataframe(matrix.style.format("{:.0%}",na_rep="—").map(lambda v: "" if pd.isna(v) else f"background-color: rgba(37,99,235,{0.12+0.45*v})"))
st.caption(tr("M0 includes acquisition. Later months measure observed activity; future periods are blank. Current month may be partial.", "M0 inclui aquisição. Os meses seguintes medem atividade observada; períodos futuros ficam vazios. O mês atual pode estar incompleto."))
st.subheader(tr("Customer explorer", "Explorador de clientes"))
selected=st.multiselect(tr("Lifecycle states", "Classificações da jornada"), sorted(states.state.unique()), default=sorted(states.state.unique()), format_func=lambda x: tr(x,state_pt.get(x,x)))
st.dataframe(states[states.state.isin(selected)])
st.download_button(tr("Export lifecycle", "Exportar ciclo de vida"),states.to_csv(index=False),"lifecycle.csv")
st.download_button(tr("Export cohorts", "Exportar coortes"),matrix.to_csv(),"cohorts.csv")


st.divider()
st.caption(tr("Rodrigo Alcantara | Analytics Intelligence Lab | Independent synthetic demonstration", "Rodrigo Alcantara | Analytics Intelligence Lab | Demonstração independente com dados sintéticos"))
st.markdown("[Data Quality](https://dgalkan-data-quality.streamlit.app) · [Decision Intelligence](https://dgalkan-decision-intelligence.streamlit.app) · [Customer Journey](https://dgalkan-customer-journey.streamlit.app)")
