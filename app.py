# app.py
"""
APP.PY
Interactive research dashboard for:
"Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock"

Author: Diyouva C. Novith
Carnegie Mellon University, Heinz College of Information Systems and Public Policy

This Streamlit app operationalizes the full research workflow described in the policy brief.
It transforms the study into an open, interactive format connecting:
1. Data (prepare.py)
2. Simulation model (simulation.py)
3. Policy interpretation (app.py)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import simulate_fee_change

st.set_page_config(page_title="H-1B / OPT / CPT Policy Simulation", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/clean_h1b_data.csv")

df = load_data()

df = load_data()

# ==============================================================
# INTRODUCTION
# ==============================================================
st.markdown(
    """
    <h1 style="text-align: center;">Modeling Post-Study Work Pathways</h1>
    <h3 style="text-align: center;">H-1B, OPT, and CPT under Policy Shock</h3>
    """,
    unsafe_allow_html=True
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

tab1, tab2, tab3 = st.tabs(["1️⃣ Data & Methodology", "2️⃣ Simulation & Results", "3️⃣ Policy Discussion & Conclusion"])

# ==============================================================
# TAB 1 – DATA & METHODOLOGY
# ==============================================================
with tab1:
    st.header("1. Data and Methodology")

    # --- Data Sources ---
    st.markdown("""
    ### Data Sources
    This study combines **three complementary datasets** to represent both the *formal* and *adaptive* sides of post-study employment:

    1. **USCIS H-1B DataHub (2015–2023)** – official records of approvals and denials for H-1B petitions.  
    2. **Fortune 500 OPT Employers (2024)** – companies employing international students through OPT.  
    3. **CPT-Friendly Employers (Day-1 CPT list)** – organizations known to hire students under CPT authorization.  

    These datasets were harmonized in `prepare.py` through a standardized workflow: employer names were normalized
    to uppercase and stripped of extra spaces; numeric fields were validated and coerced into numeric types;
    and categorical flags (`Fortune500`, `OPT_friendly`, `CPT_friendly`) were generated to indicate
    each employer’s participation across pathways.
    """)

    # --- Methodological Framework ---
    st.markdown("""
    ### Methodological Framework
    1. **Integration:** Combine all sources to map employer participation across H-1B, OPT, and CPT.  
    2. **Elasticity Modeling:** Apply an economic-elasticity approach to simulate how fee changes affect application volumes.  
    3. **Visualization:** Use Streamlit and Plotly to interpret results dynamically and transparently.  

    This mirrors the *open-source analytics* principle described in the policy brief—creating a transparent,
    reproducible framework to anticipate ripple effects and inform evidence-based reform.
    """)

    # --- Descriptive Baseline ---
    st.markdown("### Descriptive Baseline of H-1B Activity (2015–2023)")
    yearly = df.groupby("Year")[["Total_Approvals", "Total_Denials"]].sum().reset_index()

    fig1 = px.line(
        yearly, x="Year", y=["Total_Approvals", "Total_Denials"],
        markers=True, line_shape="linear",
        color_discrete_map={
            "Total_Approvals": "#4DB6AC",   # teal
            "Total_Denials": "#FF6F61"      # coral
        },
        labels={"value": "Applications", "variable": "Category"},
        title="H-1B Approvals and Denials by Year"
    )
    fig1.update_layout(template="plotly_dark", legend_title_text="Type")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    H-1B approvals fluctuate annually, but overall demand remains high—evidence of persistent employer dependence
    on foreign talent even amid policy uncertainty.
    """)

    # --- Top Employers ---
    st.subheader("Top Sponsoring Employers (All Years)")
    top_emp = (
        df.groupby("Employer")[["Total_Approvals"]]
        .sum()
        .nlargest(10, "Total_Approvals")
        .reset_index()
    )
    fig2 = px.bar(
        top_emp, x="Employer", y="Total_Approvals",
        text_auto=True,
        title="Top 10 H-1B Sponsors (2015–2023)",
        labels={"Total_Approvals": "Total Approvals"}
    )
    fig2.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Observation:**  
    Technology, finance, and consulting firms dominate H-1B sponsorship, confirming the sectoral pattern highlighted
    in the policy paper—these industries are most exposed to potential fee shocks.
    """)

    # --- Employer Overlap ---
    st.subheader("Employer Overlap Across Pathways")
    cat_summary = df.groupby("Year")[["Fortune500", "OPT_friendly", "CPT_friendly"]].sum().reset_index()

    # Optional normalization to percent of total employers per year
    employers_per_year = df.groupby("Year")["Employer_std"].nunique().reset_index(name="Total_Employers")
    cat_summary = cat_summary.merge(employers_per_year, on="Year", how="left")
    for col in ["Fortune500", "OPT_friendly", "CPT_friendly"]:
        cat_summary[col] = (cat_summary[col] / cat_summary["Total_Employers"]) * 100

    fig3 = px.line(
        cat_summary, x="Year",
        y=["Fortune500", "OPT_friendly", "CPT_friendly"],
        markers=True,
        labels={"value": "Share of Employers (%)", "variable": "Category"},
        title="Share of Employers by Category (%) – Fortune 500 / OPT / CPT"
    )
    fig3.update_layout(template="plotly_dark", legend_title_text="Category")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Interpretation:**  
    Firms appearing across multiple categories demonstrate *flexibility*—the ability to sustain hiring through OPT or CPT
    pathways when H-1B sponsorship becomes costly. The increasing share of overlapping employers over time suggests
    adaptation to policy and market shifts rather than a reduction in international talent demand.
    """)

# ==============================================================
# TAB 2 – SIMULATION & RESULTS
# ==============================================================
with tab2:
    st.header("2. Simulation of a USD 100 000 H-1B Fee")

    st.markdown("""
    ### Analytical Model
    The simulation assumes that employer demand for H-1B sponsorship is **elastic** with respect to total cost.  
    Employers react to higher sponsorship fees by reducing the number of applications they submit.

    #### Baseline Fee Assumption
    The **baseline total cost** of sponsoring an H-1B worker (government fees + legal + compliance costs) is assumed to be **USD 25 000** per worker.  
    This estimate comes from:
    - USCIS filing fees (≈ USD 6 000–10 000 for large employers)
    - Attorney and administrative costs (≈ USD 10 000–15 000)
    
    Therefore, a policy that raises the effective fee to **USD 100 000** represents a **+300 %** cost increase relative to the baseline.

    The elasticity parameter (ε) represents how responsive employers are to cost changes:
    - A value of –0.3 means a 1 % increase in cost reduces applications by 0.3 %.
    - Elasticity can vary by industry and firm size.
    """)

    # User inputs
    baseline_fee = 25_000
    fee_usd = st.slider("Set total H-1B sponsorship cost (USD)", 5_000, 100_000, 25_000, step=5_000)
    elasticity = st.slider("Elasticity (Responsiveness)", -1.0, 0.0, -0.3, step=0.05)
    st.caption(f"Elasticity interpretation: For every 1% increase in cost, applications change by {elasticity}%")

    # Compute percent change relative to baseline
    alpha = (fee_usd - baseline_fee) / baseline_fee
    sim = simulate_fee_change(df, alpha=alpha, elasticity=elasticity)

    st.markdown(f"**Simulation Parameters:** Baseline = ${baseline_fee:,} | New Fee = ${fee_usd:,} | Fee Change = {alpha*100:.1f}% | Elasticity = {elasticity}")
    st.dataframe(sim)

    if "Year" in sim.columns:
        fig_sim = px.bar(sim, x="Year", y="Change_%", color="Flexibility_Index",
                         title="Simulated Change in H-1B Applications by Employer Flexibility",
                         labels={"Change_%": "Change (%)", "Flexibility_Index": "Flexibility Index"})
        st.plotly_chart(fig_sim, use_container_width=True)

    # ----------------------------------------------------------
    # INTERPRETIVE FINDINGS
    # ----------------------------------------------------------
    projected_change = elasticity * alpha * 100
    st.markdown(f"""
    ### Key Findings
    - Increasing the effective H-1B cost to **USD {fee_usd:,}** (≈ {alpha*100:.0f} %) is projected to reduce H-1B applications by roughly **{abs(projected_change):.1f} %**, assuming elasticity = {elasticity}.
    - Employers with high flexibility—those using both OPT and CPT—are better able to adapt, shifting foreign graduates into temporary authorizations instead of filing new H-1B petitions.
    - The most adaptive sectors remain **technology, finance, and consulting**, where firms have broader visa portfolios and remote-work options.

    These simulations show that while extreme fee increases (e.g., USD 100 000) could shrink overall H-1B demand substantially, the policy effect is uneven across sectors and
    may redirect skilled labor flows rather than eliminate them.
    """)

    st.session_state.fee_usd = fee_usd
    st.session_state.elasticity = elasticity
    
# ==============================================================
# TAB 3 – POLICY DISCUSSION & CONCLUSION (Dynamic Version)
# ==============================================================
with tab3:
    st.header("3. Policy Discussion and Conclusion")

    # --- retrieve dynamic parameters from Tab 2 context ---
    # fee_usd, baseline_fee, and elasticity must be defined globally or via session_state
    baseline_fee = 25_000
    fee_usd = st.session_state.get("fee_usd", 25_000)
    elasticity = st.session_state.get("elasticity", -0.3)
    alpha = (fee_usd - baseline_fee) / baseline_fee
    projected_change = elasticity * alpha * 100

    # --- determine qualitative tone for policy interpretation ---
    if abs(projected_change) < 10:
        tone = "a mild, largely manageable adjustment"
        effect = "modest"
    elif abs(projected_change) < 40:
        tone = "a noticeable contraction in H-1B sponsorship, especially among smaller employers"
        effect = "moderate"
    else:
        tone = "a severe contraction in formal H-1B sponsorship that could reshape employer behavior"
        effect = "strong"

    # --- narrative text dynamically constructed ---
    st.markdown(f"""
    ### Policy Interpretation
    The simulation projects that increasing the total H-1B cost to **USD {fee_usd:,}**
    (≈ {alpha*100:.0f}% above baseline) would produce roughly a **{abs(projected_change):.1f}%**
    reduction in applications, given elasticity = {elasticity}.  
    This represents {tone}.

    Firms with access to **OPT** and **CPT** channels may partially offset this effect
    by reallocating international graduates to temporary work authorizations.
    The result is a redistribution of skilled labor across visa categories rather than a full collapse.
    However, at very high fee levels (e.g., ≥ USD 75 000),
    even flexible sectors begin cutting sponsorship substantially.
    """)

    st.markdown("""
    ### Policy Recommendations
    1. **Tiered H-1B Fee Structure:** Calibrate fees by employer size or wage level so smaller firms remain competitive while large firms contribute proportionally more.  
    2. **Extend STEM-OPT Duration:** Expanding from 36 to 48 months would help graduates maintain employment continuity across multiple visa cycles.  
    3. **Expand Cap-Exempt Categories:** Include universities, nonprofits, and research institutions to safeguard innovation pipelines.  
    """)

    st.markdown(f"""
    ### Broader Implications
    The H-1B, OPT, and CPT programs form a **dynamic ecosystem**.
    Shocks in one component ripple through the others, influencing employer strategy,
    compliance costs, and student career trajectories.  
    Under the current simulation, the system demonstrates **{effect} substitution dynamics**—
    some employers adapt, but overall access to foreign talent tightens as costs rise.
    """)

    st.markdown("""
    ---
    ### Conclusion
    This project underscores that:
    > **Openness to international talent, paired with evidence-based fee design,  
    remains essential to sustaining U.S. innovation and long-term growth.**

    Integrating empirical data, elasticity modeling, and open-source analytics,
    this dashboard offers a transparent and reproducible framework
    for anticipating policy ripple effects and guiding data-driven reform.
    """)