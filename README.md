# 🎓 Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock

**Author:** Diyouva C. Novith  
*Carnegie Mellon University – Heinz College of Information Systems and Public Policy*  
📄 [Policy Brief (PDF)](./policy_brief/Policy%20Brief.pdf)

---

## 🧭 Overview

This Streamlit dashboard explores how raising the **H-1B visa filing fee to USD 100 000** could affect post-study employment pathways for international graduates in the U.S.

The project combines multiple datasets and applies an **elasticity-based simulation model** to estimate how employers respond to higher sponsorship costs across three interconnected programs — **H-1B**, **Optional Practical Training (OPT)**, and **Curricular Practical Training (CPT)**.  

By pairing data exploration with simulation, the dashboard shows how policy changes may **redistribute** skilled labor rather than eliminate it.

---

## 🧩 Project Components

1. **Data Integration** – `prepare.py`  
   Cleans and merges USCIS H-1B data with OPT and CPT employer lists.  
2. **Elasticity Simulation** – `simulation.py`  
   Models how sensitive employer demand is to changes in sponsorship cost.  
3. **Policy Dashboard** – `app.py`  
   Visualizes trends, simulations, and policy implications interactively.

Together, these modules demonstrate how open-source analytics can support transparent, evidence-based policy design.

---

## 🗂️ Repository Structure
```
project/
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── h1b_datahubexport-2015.csv … 2023.csv
│   ├── fortune500_opt_companies_2024.csv
│   ├── cpt_employers_day1cptuniversities_bs4.csv
│   ├── clean_h1b_data.csv
│   ├── summary_overall.csv
│   └── sector_summary.csv
│
├── policy_brief/
│   └── Policy Brief.pdf
│
├── app.py
├── prepare.py
├── simulation.py
├── opt_company.py
├── cpt_company.py
├── requirements.txt
├── setup.sh
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Prepare the data
```bash
python prepare.py
```

### 3️⃣ Launch the dashboard
```bash
streamlit run app.py
```

You can then:
- View **H-1B approval and denial trends (2015–2023)**  
- Explore **top employers** and **sector concentration**  
- Simulate **employer responses** to fee changes**  
- Review **policy impacts** based on adaptability across visa types  

---

## 🧮 Methodology

The workflow has three main steps:

1. **Integration:** Merge H-1B, OPT, and CPT data into one employer-level dataset.  
2. **Elasticity Modeling:** Estimate how application volume changes when total cost changes.  
3. **Visualization:** Build an interactive Streamlit dashboard using Plotly.

Elasticity is modeled as:

**ΔA / A = ε × (ΔF / F)**

where:
- *A* = number of applications  
- *F* = total cost  
- *ε* = elasticity (default −0.3)

With a baseline cost of **USD 25 000**, raising fees to **USD 100 000** represents a **+300 %** increase.  
At ε = −0.3, the model projects an approximate **90 % decline** in H-1B applications.

---

## 🗃️ Analytical Outputs

The project produces two key summary files for reproducibility and further analysis:

| File | Description |
|------|--------------|
| [`data/summary_overall.csv`](./data/summary_overall.csv) | Year-by-year totals of H-1B approvals and denials (2015–2023), plus projected percentage change in applications under the USD 100 000 scenario. Used in Tab 1 (“Descriptive Baseline”) and Tab 2 (“Simulation”). |
| [`data/sector_summary.csv`](./data/sector_summary.csv) | Employer-level aggregation by sector (Technology, Finance, Consulting, etc.) showing total approvals, Fortune 500 participation, OPT/CPT friendliness, and flexibility index averages. Used in Tab 2 (“Sector Comparison”). |

These outputs allow transparent validation of all simulation and visualization results.

---

## 📊 Dashboard Tabs

| Tab | Purpose |
|-----|----------|
| **1️⃣ Data & Findings** | Shows data sources, methods, and descriptive trends such as approval rates and top employers. |
| **2️⃣ Simulation & Results** | Runs the fee-shock simulation and compares sector adaptability. |
| **3️⃣ Policy Discussion & Conclusion** | Summarizes insights, interprets results, and outlines policy options. |

---

## 📈 Key Insights (verified)

- **Demand is persistent:** H-1B applications remain strong through 2015–2023, peaking in 2023.  
- **Sponsorship is concentrated:** Large consulting/IT and tech firms account for most filings.  
- **Adaptive pathways:** **CPT-friendly** participation increases modestly; **OPT trend is not observable** due to name-matching limitations.  
- **Fee sensitivity:** At ε = −0.3 and a +300 % fee rise (USD 25 000 → 100 000), projected change ≈ **−90 %**.  
- **Sector view:** **Consulting** dominates by volume; proxies suggest large firms (often Tech/Finance) may have more flexibility, but **sector adaptability is not strongly differentiated** in current data.

---

## 🏛️ Policy Interpretation

A uniform USD 100 000 H-1B fee would lead to an estimated **90 % reduction** in applications, with uneven impacts across industries.  
Technology and finance firms can better absorb higher costs or reallocate workers through OPT/CPT channels, while consulting firms—though the largest sponsors—show lower adaptive capacity.  
This suggests that fee increases would **redirect skilled labor** rather than eliminate it entirely.

---

## 🧩 Policy Recommendations

- **Tiered H-1B Fees:** Scale by firm size or wage level to maintain small-firm competitiveness.  
- **Extend STEM-OPT Duration:** 36 → 48 months to strengthen employment continuity.  
- **Support Consulting Firms:** Encourage university partnerships and cap-exempt collaborations.  
- **Visa Transparency:** Mandate joint reporting of H-1B, OPT, and CPT utilization for evidence-based reform.

---

## 🧠 Broader Takeaways

Raising H-1B costs reshapes rather than destroys demand.  
The H-1B, OPT, and CPT programs form an interdependent ecosystem where **adaptability determines resilience**.  
Understanding this interaction is key to sustaining U.S. innovation and global competitiveness.

---

## 🧾 Citation

> **Novith, Diyouva C.** (2025). *Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock.*  
> Carnegie Mellon University, Heinz College of Information Systems and Public Policy.

APA:
```
Novith, D. C. (2025). Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock.  
Carnegie Mellon University, Heinz College of Information Systems and Public Policy.
```

---

## ✨ Acknowledgment

Developed as part of a Final Project for the **Python Programming II – Data Analysis** course at  
**Carnegie Mellon University – Heinz College of Information Systems and Public Policy**.  
This project combines empirical data, simulation modeling, and open-source visualization to promote transparent, data-driven policymaking on international talent and immigration issues.
