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
    <div style="text-align:center;">
        <h1 style="margin-bottom:-5px; font-size:40px;">Modeling Post-Study Work Pathways</h1>
        <h3 style="margin-top:-15px; font-size:23px; font-style:italic; font-weight:normal;">
            H-1B, OPT, and CPT under Policy Shock
        </h3>
        <p style="margin-top:-2px; font-size:16px; line-height:1.2;">
            <strong>Diyouva C. Novith</strong><br>
            <em>Carnegie Mellon University – Heinz College of Information Systems and Public Policy</em>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
### Introduction

International students play an indispensable role in sustaining the United States’ innovation capacity and global competitiveness. They contribute disproportionately to sectors such as **technology, finance, and research**, serving as a bridge between the nation’s higher education institutions and its advanced labor markets. Their transition from academic study to skilled employment typically occurs through three interconnected visa programs: the **H-1B**, **Optional Practical Training (OPT)**, and **Curricular Practical Training (CPT)**.

The **H-1B visa** constitutes the primary pathway for long-term employment sponsorship, allowing U.S. firms to hire foreign professionals in specialty occupations. The **OPT program** provides temporary work authorization for international graduates to gain professional experience in fields related to their academic training, while **CPT** authorizes employment that forms an integral part of a student’s curriculum. Together, these mechanisms form the backbone of the post-study work ecosystem linking U.S. universities to high-skill industries.

Recent policy discussions have introduced proposals to raise the **H-1B filing fee** to as high as **USD 100 000**, representing a substantial policy shock with potentially far-reaching consequences for employer behavior. Such an increase could deter firms from formal sponsorship, reshape hiring incentives, and intensify reliance on temporary work authorizations such as OPT and CPT.

To assess these potential impacts, this study integrates official **USCIS H-1B DataHub (2015–2023)** records with curated datasets of **OPT** and **CPT-friendly employers**. The resulting analysis provides an empirical foundation for examining how the U.S. post-study employment ecosystem might adapt under a significant cost escalation. By combining descriptive data exploration, elasticity modeling, and sector-level adaptability analysis, the research seeks to quantify not only the magnitude of the potential response but also its distribution across industries most reliant on global talent.
""")

tab1, tab2, tab3 = st.tabs(
    ["1️⃣ Data & Findings", "2️⃣ Simulation & Results", "3️⃣ Policy Discussion & Conclusion"]
)

# ==============================================================
# TAB 1 – DATA & METHODOLOGY
# ==============================================================
with tab1:
    st.header("Data and Findings")

    st.markdown("""
    ### Data Sources
    This study draws upon three complementary datasets that together capture both the formal and adaptive dimensions of post-study employment in the United States.  
    
    The primary source is the **USCIS H-1B DataHub (2015–2023)**, which provides official records of petition approvals and denials and serves as the foundation for analyzing formal employer sponsorship patterns.  
    
    To represent adaptive pathways that operate alongside H-1B, the analysis incorporates the **Fortune 500 OPT Employers (2024)** dataset—containing major U.S. companies that employ international students under Optional Practical Training (OPT) authorization—and the **CPT-Friendly Employers (Day-1 CPT list)**, which identifies institutions and firms known to hire students through Curricular Practical Training (CPT).  
    
    These sources were harmonized through a standardized preprocessing workflow implemented in `prepare.py`, where employer names were normalized to a consistent format, numeric variables were validated, and categorical indicators (`Fortune500`, `OPT_friendly`, and `CPT_friendly`) were generated to denote each firm’s participation across post-study pathways.
    """)

    st.markdown("""
    ### Methodological Framework
    The methodological design proceeds in three stages:  
    
    The first stage, **integration**, combines the three datasets to create a unified map of employer participation across H-1B, OPT, and CPT programs, enabling cross-pathway comparisons.  
    
    The second stage, **elasticity modeling**, applies an economic-elasticity approach to estimate how changes in total sponsorship cost affect employer application behavior, capturing the responsiveness of demand to fee shocks.  

    Finally, the **visualization** stage translates these analytical results into an interactive, reproducible format using Streamlit and Plotly, ensuring transparency and accessibility for both policy analysts and academic audiences.
    """)

    # --- Chart 1: Baseline trends ---
    st.markdown("### Descriptive Baseline of H-1B Activity (2015–2023)")
    yearly = df.groupby("Year")[["Total_Approvals", "Total_Denials"]].sum().reset_index()
    fig1 = px.line(
        yearly, x="Year", y=["Total_Approvals", "Total_Denials"],
        markers=True,
        color_discrete_map={"Total_Approvals": "#4DB6AC", "Total_Denials": "#FF6F61"},
        labels={"value": "Applications", "variable": "Category"},
        title="H-1B Approvals and Denials by Year"
    )
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    *Chart 1 – H-1B Approvals and Denials (2015–2023):*  
    The chart shows that overall employer demand for H-1B sponsorship has remained strong and resilient from 2015 to 2023, even as approval and denial rates fluctuated under changing policy conditions.  
    Approvals rose steadily until 2022, while denials spiked briefly during periods of stricter review.  
    Despite these fluctuations, the total volume of applications never collapsed, illustrating a **structural dependence on foreign skilled labor**.  
    This persistence establishes a baseline of **inelastic demand**, supporting later simulations of how only extreme fee increases would meaningfully reduce participation.
    """)

    # --- Chart 2: Top employers ---
    st.subheader("Top Sponsoring Employers (All Years)")
    top_emp = df.groupby("Employer")[["Total_Approvals"]].sum().nlargest(10, "Total_Approvals").reset_index()
    fig2 = px.bar(
        top_emp, x="Employer", y="Total_Approvals", text_auto=True,
        title="Top 10 H-1B Sponsors (2015–2023)",
        labels={"Total_Approvals": "Total Approvals"}
    )
    fig2.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    *Chart 2 – Top Employers:*  
    The bar chart reveals that **H-1B sponsorship is highly concentrated among large consulting and technology firms** such as Cognizant, Tata Consultancy Services, Infosys, Microsoft, and Deloitte.  
    This concentration pattern shows that the H-1B program is structurally anchored in **knowledge-intensive sectors** reliant on global STEM talent.  
    The dominance of these firms implies that any future fee shock would disproportionately affect these industries, yet their broad visa management capacity and diversified authorization strategies suggest **lower elasticity**—they can absorb higher costs more effectively than smaller employers.  
    This concentration provides the empirical foundation for the **sectoral adaptability analysis** introduced in Tab 2.
    """)

    # --- Chart 3: Employer participation across pathways ---
    st.subheader("Employer Participation Across Pathways")
    cat_summary = df.groupby("Year")[["Fortune500", "OPT_friendly", "CPT_friendly"]].sum().reset_index()
    employers_per_year = df.groupby("Year")["Employer_std"].nunique().reset_index(name="Total_Employers")
    cat_summary = cat_summary.merge(employers_per_year, on="Year", how="left")
    for col in ["Fortune500", "OPT_friendly", "CPT_friendly"]:
        cat_summary[col] = (cat_summary[col] / cat_summary["Total_Employers"]) * 100

    fig3 = px.line(
        cat_summary, x="Year",
        y=["Fortune500", "OPT_friendly", "CPT_friendly"],
        markers=True,
        labels={"value": "Share of Employers (%)", "variable": "Category"},
        title="Share of Employers by Category (%)"
    )
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    *Chart 3 – Employer Participation Across Pathways:*  
    This line chart tracks the share of employers classified as **Fortune 500**, **OPT-friendly**, or **CPT-friendly** from 2015 to 2023.  
    Although each line represents a separate category rather than a direct overlap, the simultaneous upward trends—especially among Fortune 500 and CPT-friendly firms—indicate that major employers increasingly engage with **alternative visa pathways** alongside formal H-1B sponsorship.  
    This broadening participation suggests a gradual institutionalization of flexibility within U.S. hiring practices: firms are diversifying their authorization channels to ensure continued access to international talent amid regulatory or cost uncertainty.  
    This behavioral pattern provides a conceptual bridge to Tab 2, where elasticity modeling quantifies how such flexibility moderates the impact of fee shocks.
    """)

# ==============================================================
# TAB 2 – SIMULATION & SECTOR RESULTS
# ==============================================================
with tab2:
    st.header("Simulation of a USD 100 000 H-1B Fee")

    # --- Baseline setup ---
    baseline_fee = 25_000
    st.markdown("""
    **Interactive Filters**  
    Use the sliders below to test different H-1B fee levels and employer responsiveness.  
    The chart dynamically illustrates how flexibility affects the magnitude of the decline in applications.
    """)

    # --- User inputs ---
    fee_usd = st.slider(
        "Set total H-1B sponsorship cost (USD)",
        5_000, 100_000, 25_000, step=5_000
    )

    elasticity = st.slider(
        "Average Elasticity (Responsiveness, ε)",
        -1.0, 0.0, -0.3, step=0.05,
        help="Overall responsiveness of employers to fee changes"
    )

    # --- Automatically create heterogeneity ---
    elasticity_gap = 0.15  # how much low/high differ from average
    elasticity_low = max(-1.0, elasticity - elasticity_gap)   # less flexible employers
    elasticity_high = min(0.0, elasticity + elasticity_gap)   # more flexible employers

    # --- Compute proportional fee change ---
    alpha = (fee_usd - baseline_fee) / baseline_fee

    # --- Run simulation with heterogeneous elasticity ---
    sim = simulate_fee_change(
        df,
        alpha=alpha,
        elasticity_low=elasticity_low,
        elasticity_high=elasticity_high
    )

    # ==============================================================
    # TWO-COLUMN PARAMETER SUMMARY
    # ==============================================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="font-family:Georgia; color:#2b2b2b; font-size:16px;">
                <b>Policy Inputs</b><br>
                <ul style="margin-top:5px; line-height:1.6;">
                    <li><b>Baseline Fee:</b> ${baseline_fee:,.0f}</li>
                    <li><b>New Fee:</b> ${fee_usd:,.0f}</li>
                    <li><b>Fee Change (α):</b> {alpha*100:.1f}%</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="font-family:Georgia; color:#2b2b2b; font-size:16px;">
                <b>Elasticity (ε)</b><br>
                <ul style="margin-top:5px; line-height:1.6;">
                    <li><b>Less Flexible:</b> {elasticity_low:.2f}</li>
                    <li><b>More Flexible:</b> {elasticity_high:.2f}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Optional divider line
    st.markdown("<hr style='margin-top:0px; margin-bottom:20px;'>", unsafe_allow_html=True)

    # --- Optional summary metric ---
    projected_change_low = elasticity_low * alpha * 100
    projected_change_high = elasticity_high * alpha * 100

    st.markdown(
        f"""
        <div style="text-align:center; font-family:Georgia; color:#2b2b2b;">
            <div style="font-size:16px; font-weight:bold;">
                Projected Change Range (Δ Applications, %)
            </div>
            <div style="font-size:32px; font-weight:bold; margin-top:6px;">
                {projected_change_high:.1f}% to {projected_change_low:.1f}%
            </div>
            <div style="font-size:14px; color:#555;">
                Expected reduction in applications from more vs. less flexible employers
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==============================================================
    # VISUALIZATION
    # ==============================================================
    custom_palette = ["#c4452f", "#6b705c"]  # red = less flexible, green-gray = more flexible

    if "Year" in sim.columns and "Flex_Group" in sim.columns:
        fig_sim = px.bar(
            sim,
            x="Year",
            y="Change_%",
            color="Flex_Group",
            barmode="group",
            labels={
                "Change_%": "Change (%)",
                "Flex_Group": "Employer Flexibility",
                "Year": "Year"
            },
            color_discrete_sequence=custom_palette,
        )

        # --- Title and layout ---
        fig_sim.update_layout(
            title=dict(
                text=(
                    "<span style='font-size:22px; font-family:Georgia; font-weight:bold;'>"
                    "Employers with greater flexibility exhibit smaller declines in H-1B applications under rising fees."
                    "</span><br>"
                    "<span style='font-size:18px; font-family:Georgia; font-weight:bold; font-style:italic;'>"
                    "Simulated Change in H-1B Applications by Employer Flexibility"
                    "</span>"
                ),
                x=0.5,
                xanchor="center",
                y=0.95
            ),
            template="simple_white",
            font=dict(family="Georgia", color="#2b2b2b"),
            xaxis_title="",
            yaxis_title=None,
            legend_title_text="",  # remove legend title
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            bargap=0.25,
            margin=dict(t=120, b=60, l=30, r=30),
        )

        # --- Axis and label cleanup ---
        fig_sim.update_yaxes(visible=False, showticklabels=False, showgrid=False, zeroline=False)
        fig_sim.update_xaxes(showgrid=False, linecolor="rgba(0,0,0,0.3)", tickfont=dict(size=14))
        fig_sim.update_traces(
            texttemplate="%{y:.1f}%",
            textposition="outside",
            textfont=dict(family="Georgia", size=14, color="#2b2b2b"),
            cliponaxis=False
        )

        st.plotly_chart(fig_sim, use_container_width=True)

        st.markdown("""
        The simulation indicates that the decline in H-1B applications resulting from fee increases varies systematically across employers. Firms characterized by higher flexibility show a significantly smaller reduction in application volume, suggesting that adaptive capacity enables them to absorb policy-induced cost pressures more effectively. This pattern reveals a structural asymmetry in the labor market response: while less flexible employers retract sharply in the face of rising costs, more adaptable organizations maintain a steadier level of engagement. Such heterogeneity underscores the importance of organizational adaptability as a moderating factor in policy transmission and highlights how fee-based interventions can have uneven effects across employer types.
        """)
        st.markdown("<br><br>", unsafe_allow_html=True)

    # --- Sector Analysis ---
    st.markdown("""
    <div style="text-align:center; font-family:Georgia; color:#2b2b2b;">
        <div style="font-size:22px; font-weight:bold; margin-bottom:2px;">
            Industries that diversify visa channels—like Finance and Technology—absorb cost shocks far better than sectors dependent solely on H-1B sponsorship.
        </div>
        <div style="font-size:18px; font-style:italic; margin-top:2px;">
            Sector-Level Evidence from H-1B Data
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Sector mapping ---
    df["NAICS2"] = (df["NAICS"].astype(str).str[:2]).astype(int)
    naics_map = {
        51: "Technology (Information)",
        52: "Finance/Insurance",
        54: "Professional/Consulting",
        55: "Management of Companies",
        61: "Education",
        62: "Healthcare/Social Assistance",
        31: "Manufacturing",
        32: "Manufacturing",
        33: "Manufacturing",
    }
    df["Sector"] = df["NAICS2"].map(naics_map).fillna("Other")

    # --- Aggregate and normalize ---
    sector_summary = (
        df.groupby("Sector")
        .agg(
            Total_Approvals=("Total_Approvals", "sum"),
            mean_flex=("Flexibility_Index", "mean"),
            share_opt=("OPT_friendly", "mean"),
            share_cpt=("CPT_friendly", "mean"),
            share_f500=("Fortune500", "mean"),
        )
        .reset_index()
    )

    for col in ["mean_flex", "share_opt", "share_cpt", "share_f500"]:
        denom = (sector_summary[col].max() - sector_summary[col].min()) or 1e-9
        sector_summary[col + "_norm"] = (sector_summary[col] - sector_summary[col].min()) / denom

    sector_summary["adaptive_score"] = sector_summary[
        ["mean_flex_norm", "share_opt_norm", "share_cpt_norm", "share_f500_norm"]
    ].mean(axis=1)

    # --- Top 10 sectors ---
    top_approvals = sector_summary.sort_values("Total_Approvals", ascending=True).tail(10)
    top_adapt = sector_summary.sort_values("adaptive_score", ascending=True).tail(10)

    # --- Theme colors ---
    color_approvals = "#4DB6AC"  # teal
    color_adaptive = "#E4A672"   # warm tan

    col1, col2 = st.columns(2)

    with col1:
        fig_approvals = px.bar(
            top_approvals,
            y="Sector",
            x="Total_Approvals",
            text="Total_Approvals",
            orientation="h",
            color_discrete_sequence=[color_approvals],
            labels={"Total_Approvals": "Total Approvals", "Sector": ""},
            title="<b>Top Sectors by H-1B Approvals</b>",
        )
        fig_approvals.update_traces(
            texttemplate="%{x:,.0f}",
            textposition="outside",
            marker_line_color="#2b2b2b",
            marker_line_width=0.8,
        )
        fig_approvals.update_layout(
            template="simple_white",
            font=dict(family="Georgia", color="#2b2b2b"),
            yaxis=dict(title="", showgrid=False, showticklabels=True),
            xaxis=dict(title="", showgrid=True, gridcolor="rgba(0,0,0,0.05)", visible=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=70, b=60, l=20, r=40),
        )
        st.plotly_chart(fig_approvals, use_container_width=True)

    with col2:
        fig_adaptive = px.bar(
            top_adapt,
            y="Sector",
            x="adaptive_score",
            text="adaptive_score",
            orientation="h",
            color_discrete_sequence=[color_adaptive],
            labels={"adaptive_score": "Adaptive Score", "Sector": ""},
            title="<b>Top Sectors by Adaptive Score</b>",
        )
        fig_adaptive.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            marker_line_color="#2b2b2b",
            marker_line_width=0.8,
        )
        fig_adaptive.update_layout(
            template="simple_white",
            font=dict(family="Georgia", color="#2b2b2b"),
            yaxis=dict(title="", showgrid=False, showticklabels=True),
            xaxis=dict(title="", showgrid=True, gridcolor="rgba(0,0,0,0.05)", visible=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=70, b=60, l=20, r=40),
        )
        st.plotly_chart(fig_adaptive, use_container_width=True)

    st.markdown("""
    *Charts 5 & 6 – Sector Comparison:*  
    The left chart shows which industries file the most petitions (scale of dependence).  
    The right chart ranks sectors by composite adaptability, combining flexibility indices and OPT/CPT overlap.  
    Together they reveal that **Technology and Finance** have the highest adaptive capacity,  
    while **Consulting** dominates by size but adapts less efficiently.
    """)

    st.markdown(f"""
    ### Key Findings
    - Raising H-1B cost to **USD {fee_usd:,}** (~{alpha*100:.0f}% above baseline) reduces applications by roughly **{abs(projected_change_high):.1f}% to {abs(projected_change_low):.1f}%**, depending on employer flexibility.  
    - Employers with broad visa portfolios offset this via OPT/CPT.  
    - **Technology and Finance** are most adaptive; **Consulting** leads by volume but faces adjustment risk.
    """)

    st.session_state.fee_usd = fee_usd
    st.session_state.elasticity = elasticity

# ==============================================================
# TAB 3 – POLICY DISCUSSION & CONCLUSION
# ==============================================================
with tab3:
    st.header("Policy Discussion and Conclusion")

    baseline_fee = 25_000
    fee_usd = st.session_state.get("fee_usd", 25_000)
    elasticity = st.session_state.get("elasticity", -0.3)
    alpha = (fee_usd - baseline_fee) / baseline_fee
    
    # Average elasticity proxy for overall change narrative
    projected_change = ((elasticity_high + elasticity_low) / 2) * alpha * 100

    if abs(projected_change) < 10:
        tone = "a mild and manageable adjustment in employer demand"
        effect = "modest"
    elif abs(projected_change) < 40:
        tone = "a noticeable contraction, particularly among smaller or less flexible employers"
        effect = "moderate"
    else:
        tone = "a severe contraction that could reshape sponsorship patterns"
        effect = "strong"

    st.markdown(f"""
    ### Policy Interpretation

    The simulation results suggest that increasing the total H-1B sponsorship cost to **USD {fee_usd:,}**
    (approximately **{alpha*100:.0f}%** above the current baseline) would result in an estimated
    **{abs(projected_change):.1f}%** reduction in overall H-1B applications, assuming an elasticity of **{elasticity}**.
    This outcome represents {tone}, implying that employer responses to policy shocks are not uniform across the economy.
    Rather, the degree of adjustment depends heavily on each sector’s flexibility and capacity to absorb increased costs.

    The **Technology (Information)** and **Finance/Insurance** sectors exhibit the highest adaptability scores in the dataset,
    suggesting that firms within these industries can more readily adjust to elevated sponsorship costs by reallocating workers
    through alternative visa pathways such as **OPT** or **CPT**. In contrast, **Professional and Consulting** firms remain
    the largest contributors to total H-1B petitions but demonstrate relatively lower adaptive capacity,
    indicating greater vulnerability to sharp fee increases. These findings underscore the asymmetric impact of cost shocks
    across industries, revealing that elevated fees are likely to **redirect skilled labor flows** rather than eliminate them entirely.
    """)

    st.markdown("""
    ### Policy Implications and Recommendations

    The empirical and simulated results collectively suggest that policy instruments affecting the H-1B program
    should be designed with sectoral heterogeneity in mind. A uniform fee increase risks amplifying disparities between
    large, flexible employers and smaller firms that lack access to alternative visa portfolios.  

    First, a **tiered H-1B fee structure**—scaled according to employer size or prevailing wage level—could preserve access
    for small and mid-sized enterprises while ensuring that larger corporations contribute proportionally more.  
    
    Second, extending the **STEM-OPT duration** from 36 to 48 months would strengthen short-term employment continuity for
    graduates in high-demand disciplines such as technology and finance, mitigating the transition pressure from OPT to H-1B status.  
    
    Third, targeted support for **consulting and professional service firms** through university partnerships and cap-exempt collaborations
    could sustain participation in the high-skill labor market while easing adjustment burdens.  
    
    Finally, establishing **visa portfolio transparency**, requiring joint reporting of H-1B, OPT, and CPT utilization,
    would enhance evidence-based policy evaluation and future reform design.
    """)

    st.markdown(f"""
    ### Broader Implications

    The combined evidence from elasticity modeling and sector-level adaptability points to **{effect} substitution dynamics**
    within the post-study employment ecosystem. Rather than a collapse in foreign talent inflows, the results suggest
    a reallocation process in which more adaptive sectors absorb displaced demand through alternative visa channels.
    The three programs—H-1B, OPT, and CPT—thus function as **a single interdependent system**, where adaptability determines
    both sectoral resilience and the aggregate capacity to sustain skilled labor supply under policy stress.
    """)

    st.markdown("""
    ---
    ### Conclusion

    This study demonstrates that **Technology** and **Finance** remain the most adaptive sectors under simulated H-1B fee shocks,
    whereas **Consulting** continues to dominate sponsorship volume but faces greater structural constraints.
    Policymakers should recognize that openness to international talent and the flexibility of post-study employment programs
    are complementary drivers of U.S. competitiveness.  
    
    Data-driven calibration of visa fees and program durations, coupled with transparency across employment pathways,
    is essential to preserving both economic dynamism and equitable access to skilled labor opportunities.
    """)