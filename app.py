# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import simulate_fee_change

st.set_page_config(page_title="H1B Simulation App", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("clean_h1b_data.csv")

st.title("H-1B Policy Simulation Dashboard")

df = load_data()

tab1, tab2 = st.tabs(["Overview", "Fee Simulation"])

with tab1:
    st.subheader("Total H-1B Approvals by Year")
    yearly = df.groupby("Year")[["Total_Approvals", "Total_Denials"]].sum().reset_index()
    fig = px.line(yearly, x="Year", y=["Total_Approvals", "Total_Denials"], markers=True,
                  labels={"value": "Applications", "variable": "Type"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Employers")
    top_emp = df.groupby("Employer")[["Total_Approvals"]].sum().nlargest(10, "Total_Approvals").reset_index()
    fig_top = px.bar(top_emp, x="Employer", y="Total_Approvals", title="Top 10 Employers by Approvals",
                     labels={"Total_Approvals": "Total Approvals"}, text_auto=True)
    st.plotly_chart(fig_top, use_container_width=True)

    st.subheader("Category Breakdown")
    cat_summary = df.groupby("Year")[["Fortune500", "OPT_friendly", "CPT_friendly"]].sum().reset_index()
    fig_cat = px.line(cat_summary, x="Year",
                      y=["Fortune500", "OPT_friendly", "CPT_friendly"],
                      markers=True, title="Employer Category Over Time")
    st.plotly_chart(fig_cat, use_container_width=True)

with tab2:
    st.subheader("Simulate Fee Change")
    alpha = st.slider("Fee Change (%)", -50, 50, 0) / 100
    elasticity = st.slider("Elasticity", -1.0, 0.0, -0.3)
    sim = simulate_fee_change(df, alpha=alpha, elasticity=elasticity)
    st.dataframe(sim)

    st.subheader("Simulation Result by Category")
    fig_sim = px.bar(sim, x="Year", y="Change_%", color="Flexibility_Index",
                     title="Simulated Change in Applications by Employer Flexibility",
                     labels={"Change_%": "Change (%)", "Flexibility_Index": "Flexibility Index"})
    st.plotly_chart(fig_sim, use_container_width=True)