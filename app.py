"""
# app.py

Interactive Research Dashboard for:
**"Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock"**

Author: **Diyouva C. Novith**  
Carnegie Mellon University – Heinz College of Information Systems and Public Policy

---

### Overview
This Streamlit app operationalizes the full workflow from the accompanying policy brief:
- Integrates official **USCIS H-1B data (2015–2023)** with employer lists for **OPT** and **CPT**
- Simulates the impact of a **USD 100 000 H-1B fee shock** using elasticity modeling
- Analyzes **sector-level adaptability** based on NAICS industry codes and employer flexibility indices

The dashboard connects three analytical components:
1. **Data Integration** – implemented in `prepare.py`  
2. **Elasticity Simulation** – implemented in `simulation.py`  
3. **Sector & Policy Interpretation** – implemented here in `app.py`

This app embodies the principle of **open, reproducible research**, enabling users to
interactively explore how U.S. post-study work pathways might adapt to major policy shifts.
"""

# ==============================================================
# Imports and configuration
# ==============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import simulate_fee_change

st.set_page_config(page_title="H-1B / OPT / CPT Policy Simulation", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/clean_h1b_data.csv")

df = load_data()

# ==============================================================
# INTRODUCTION
# ==============================================================
st.markdown(
    """
    <h1 style="text-align:center;">Modeling Post-Study Work Pathways</h1>
    <h3 style="text-align:center;">H-1B, OPT, and CPT under Policy Shock</h3>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
### Introduction
International students are central to U.S. innovation and competitiveness.  
They fill critical roles in **technology, finance, and research**, linking higher education to the labor market
through **three interconnected programs**:

- **H-1B visa** – formal employer sponsorship for skilled workers.  
- **OPT (Optional Practical Training)** – temporary authorization for graduates to gain work experience.  
- **CPT (Curricular Practical Training)** – employment authorization integrated with academic study.

Recent proposals to raise the H-1B filing fee to **USD 100 000** represent a potential policy shock.
Such a dramatic increase could discourage employers from sponsorship, change hiring incentives,
and increase reliance on temporary pathways like OPT and CPT.

This project integrates official USCIS data with scraped employer lists for OPT and CPT to explore
how the **ecosystem of post-study employment** might adapt under this cost increase.
""")

tab1, tab2, tab3 = st.tabs(
    ["1️⃣ Data & Methodology", "2️⃣ Simulation & Results", "3️⃣ Policy Discussion & Conclusion"]
)

# ==============================================================
# TAB 1 – DATA & METHODOLOGY
# ==============================================================
with tab1:
    st.header("1. Data and Methodology")

    st.markdown("""
    ### Data Sources
    This study combines **three complementary datasets** representing both the *formal* and *adaptive* sides of post-study employment:

    1. **USCIS H-1B DataHub (2015–2023)** – official records of approvals and denials.  
    2. **Fortune 500 OPT Employers (2024)** – companies employing international students through OPT.  
    3. **CPT-Friendly Employers (Day-1 CPT list)** – organizations known to hire students under CPT authorization.  

    These datasets were harmonized in `prepare.py`: employer names were standardized,
    numeric columns validated, and indicator flags (`Fortune500`, `OPT_friendly`, `CPT_friendly`)
    created to denote participation across pathways.
    """)

    st.markdown("""
    ### Methodological Framework
    1. **Integration** – combine all sources to map employer participation across H-1B, OPT, and CPT.  
    2. **Elasticity Modeling** – simulate how fee changes affect application volumes.  
    3. **Visualization** – use Streamlit and Plotly for transparent, reproducible interpretation.  
    """)

    st.markdown("### Descriptive Baseline of H-1B Activity (2015–2023)")
    yearly = df.groupby("Year")[["Total_Approvals","Total_Denials"]].sum().reset_index()
    fig1 = px.line(
        yearly, x="Year", y=["Total_Approvals","Total_Denials"],
        markers=True, color_discrete_map={"Total_Approvals":"#4DB6AC","Total_Denials":"#FF6F61"},
        labels={"value":"Applications","variable":"Category"},
        title="H-1B Approvals and Denials by Year"
    )
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    *Chart 1 – H-1B Approvals and Denials (2015–2023):*  
    This line chart tracks the annual totals of approvals and denials reported by USCIS.  
    Hover to inspect exact counts; peaks correspond to high-demand fiscal years.  
    Use this as a baseline for understanding macro-level volatility in sponsorship demand.
    """)

    st.subheader("Top Sponsoring Employers (All Years)")
    top_emp = df.groupby("Employer")[["Total_Approvals"]].sum().nlargest(10,"Total_Approvals").reset_index()
    fig2 = px.bar(
        top_emp, x="Employer", y="Total_Approvals", text_auto=True,
        title="Top 10 H-1B Sponsors (2015–2023)",
        labels={"Total_Approvals":"Total Approvals"}
    )
    fig2.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    *Chart 2 – Top 10 Employers:*  
    This bar chart highlights the firms filing the most H-1B petitions across all years.  
    It reveals employer concentration in consulting, technology, and finance sectors—industries most exposed to fee shocks.
    """)

    st.markdown("""
    **Observation:**  
    The largest sponsors are concentrated in **Professional/Consulting**, **Technology**, and **Finance**.  
    Consulting dominates by total volume, while technology and finance show greater overlap with **OPT**/**CPT** pathways—an early indicator of adaptability explored later.
    """)

    st.subheader("Employer Overlap Across Pathways")
    cat_summary = df.groupby("Year")[["Fortune500","OPT_friendly","CPT_friendly"]].sum().reset_index()
    employers_per_year = df.groupby("Year")["Employer_std"].nunique().reset_index(name="Total_Employers")
    cat_summary = cat_summary.merge(employers_per_year,on="Year",how="left")
    for col in ["Fortune500","OPT_friendly","CPT_friendly"]:
        cat_summary[col] = (cat_summary[col]/cat_summary["Total_Employers"])*100
    fig3 = px.line(
        cat_summary, x="Year", y=["Fortune500","OPT_friendly","CPT_friendly"],
        markers=True, labels={"value":"Share of Employers (%)","variable":"Category"},
        title="Share of Employers by Category (%)"
    )
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    *Chart 3 – Employer Overlap:*  
    Each line shows the percentage of employers in Fortune 500, OPT-friendly, or CPT-friendly categories.  
    The rising OPT/CPT curves suggest growing reliance on adaptive work authorizations beyond H-1B.
    """)

# ==============================================================
# TAB 2 – SIMULATION & SECTOR RESULTS
# ==============================================================
with tab2:
    st.header("2. Simulation of a USD 100 000 H-1B Fee")

    baseline_fee = 25_000
    st.markdown("""
    **Interactive Filters**  
    Use the sliders below to test different H-1B fee levels and elasticity assumptions.  
    The results will update automatically to show how sensitive total applications are to these parameters.
    """)
    fee_usd = st.slider("Set total H-1B sponsorship cost (USD)",5_000,100_000,25_000,step=5_000)
    elasticity = st.slider("Elasticity (Responsiveness)",-1.0,0.0,-0.3,step=0.05)
    alpha = (fee_usd - baseline_fee) / baseline_fee
    sim = simulate_fee_change(df, alpha=alpha, elasticity=elasticity)
    projected_change = elasticity * alpha * 100

    st.markdown(f"""
    **Simulation Parameters:**  
    Baseline = ${baseline_fee:,} | New Fee = ${fee_usd:,} | Fee Change = {alpha*100:.1f}% | Elasticity = {elasticity}
    """)

    if "Year" in sim.columns:
        fig_sim = px.bar(
            sim, x="Year", y="Change_%", color="Flexibility_Index",
            title="Simulated Change in H-1B Applications by Employer Flexibility",
            labels={"Change_%":"Change (%)","Flexibility_Index":"Flexibility Index"}
        )
        fig_sim.update_layout(template="plotly_dark")
        st.plotly_chart(fig_sim, use_container_width=True)

        st.markdown("""
        *Chart 4 – Fee Impact Simulation:*  
        Bars represent percentage change in applications per year, shaded by employer flexibility.  
        Darker colors = higher flexibility = smaller decline.  
        This visualization quantifies how adaptable employers cushion the effect of rising fees.
        """)

    # --- Sector Analysis ---
    st.markdown("### Sector-Level Evidence from H-1B Data")
    df["NAICS2"] = (df["NAICS"].astype(str).str[:2]).astype(int)
    naics_map = {
        51:"Technology (Information)",52:"Finance/Insurance",54:"Professional/Consulting",
        55:"Management of Companies",61:"Education",62:"Healthcare/Social Assistance",
        31:"Manufacturing",32:"Manufacturing",33:"Manufacturing"
    }
    df["Sector"] = df["NAICS2"].map(naics_map).fillna("Other")

    sector_summary = (
        df.groupby("Sector")
        .agg(Total_Approvals=("Total_Approvals","sum"),
             mean_flex=("Flexibility_Index","mean"),
             share_opt=("OPT_friendly","mean"),
             share_cpt=("CPT_friendly","mean"),
             share_f500=("Fortune500","mean"))
        .reset_index()
    )

    for col in ["mean_flex","share_opt","share_cpt","share_f500"]:
        denom = (sector_summary[col].max()-sector_summary[col].min()) or 1e-9
        sector_summary[col+"_norm"]=(sector_summary[col]-sector_summary[col].min())/denom
    sector_summary["adaptive_score"]=sector_summary[
        ["mean_flex_norm","share_opt_norm","share_cpt_norm","share_f500_norm"]
    ].mean(axis=1)

    top_approvals=sector_summary.sort_values("Total_Approvals",ascending=False).head(10)
    top_adapt=sector_summary.sort_values("adaptive_score",ascending=False).head(10)

    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(
            px.bar(top_approvals,x="Sector",y="Total_Approvals",text_auto=True,
                   title="Top Sectors by H-1B Approvals",
                   color_discrete_sequence=["#4DB6AC"]).update_layout(template="plotly_dark"),
            use_container_width=True)
    with col2:
        st.plotly_chart(
            px.bar(top_adapt,x="Sector",y="adaptive_score",text_auto=True,
                   title="Top Sectors by Adaptive Score",
                   color_discrete_sequence=["#FFB74D"]).update_layout(template="plotly_dark"),
            use_container_width=True)

    st.markdown("""
    *Charts 5 & 6 – Sector Comparison:*  
    The left chart shows which industries file the most petitions (scale of dependence).  
    The right chart ranks sectors by composite adaptability, combining flexibility indices and OPT/CPT overlap.  
    Together they reveal that **Technology and Finance** have the highest adaptive capacity,  
    while **Consulting** dominates by size but adapts less efficiently.
    """)

    st.markdown(f"""
    ### Key Findings
    - Raising H-1B cost to **USD {fee_usd:,}** (~{alpha*100:.0f}% above baseline) reduces applications ≈ **{abs(projected_change):.1f}%**.  
    - Employers with broad visa portfolios offset this via OPT/CPT.  
    - **Technology and Finance** are most adaptive; **Consulting** leads by volume but faces adjustment risk.
    """)

    st.session_state.fee_usd = fee_usd
    st.session_state.elasticity = elasticity

# ==============================================================
# TAB 3 – POLICY DISCUSSION & CONCLUSION
# ==============================================================
with tab3:
    st.header("3. Policy Discussion and Conclusion")

    baseline_fee = 25_000
    fee_usd = st.session_state.get("fee_usd",25_000)
    elasticity = st.session_state.get("elasticity",-0.3)
    alpha = (fee_usd - baseline_fee) / baseline_fee
    projected_change = elasticity * alpha * 100

    if abs(projected_change)<10:
        tone="a mild, manageable adjustment in employer demand"
        effect="modest"
    elif abs(projected_change)<40:
        tone="a noticeable contraction, particularly among smaller or less flexible employers"
        effect="moderate"
    else:
        tone="a severe contraction that could reshape sponsorship patterns"
        effect="strong"

    st.markdown(f"""
    ### Policy Interpretation
    Increasing the total H-1B cost to **USD {fee_usd:,}** (≈ {alpha*100:.0f}% above baseline) is projected to reduce applications by ≈ **{abs(projected_change):.1f}%**, indicating {tone}.  
    **Technology (Information)** and **Finance/Insurance** show the highest adaptability scores, while **Professional/Consulting** dominates by volume but has mixed resilience.
    """)

    st.markdown("""
    *Interpretive Note:*  
    This narrative synthesizes data from all prior charts—linking cost sensitivity (Chart 4)  
    with sector adaptability (Charts 5–6) to provide a holistic policy perspective.
    """)

    st.markdown("""
    ### Policy Recommendations
    1. **Tiered H-1B Fee Structure** – scale by employer size or wage level to preserve access for smaller firms.  
    2. **Extend STEM-OPT Duration** – from 36 to 48 months to support continuity in tech and finance.  
    3. **Support Consulting Firms** – encourage university and cap-exempt partnerships to offset fee burdens.  
    4. **Visa Portfolio Transparency** – require joint reporting of H-1B/OPT/CPT usage to inform future reforms.
    """)

    st.markdown(f"""
    ### Broader Implications
    The combined model and sector evidence show **{effect} substitution dynamics**: higher costs redirect international graduates toward sectors with stronger alternative visa options rather than eliminate demand.  
    The three pathways form an interconnected ecosystem where adaptability determines resilience to policy shocks.
    """)

    st.markdown("""
    ---
    ### Conclusion
    > **Technology and Finance remain the most adaptive sectors under H-1B fee shocks**,  
    > while **Consulting** remains the largest sponsor but faces greater adjustment risks.

    Evidence-based fee design and temporary program extensions are crucial to preserving U.S. innovation capacity and global talent access.
    """)