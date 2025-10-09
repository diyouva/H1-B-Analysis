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
│   └── clean_h1b_data.csv
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
- Simulate **employer responses** to fee changes  
- Review **policy impacts** based on adaptability across visa types  

---

## 🧮 Methodology

The workflow has three main steps:

1. **Integration:** Merge H-1B, OPT, and CPT data into one employer-level dataset.  
2. **Elasticity Modeling:** Estimate how application volume changes when total cost changes.  
3. **Visualization:** Build an interactive Streamlit dashboard using Plotly.

Elasticity is modeled as:
\[
\frac{\Delta A}{A} = \varepsilon \times \frac{\Delta F}{F}
\]
where \(A\) = applications, \(F\) = cost, and \(\varepsilon\) = elasticity (default −0.3).

---

## 📊 Dashboard Tabs

| Tab | Purpose |
|-----|----------|
| **1️⃣ Data & Findings** | Shows data sources, methods, and descriptive trends such as approval rates and top employers. |
| **2️⃣ Simulation & Results** | Runs the fee-shock simulation and compares sector adaptability. |
| **3️⃣ Policy Discussion & Conclusion** | Summarizes insights, interprets results, and outlines policy options. |

---

## 📈 Key Insights

- **Demand is persistent:** H-1B applications stay strong even through restrictive periods.  
- **Sponsorship is concentrated:** Consulting and tech firms drive most petitions.  
- **Firms are adapting:** OPT- and CPT-friendly employers are growing in share.  
- **Fee sensitivity is uneven:** A USD 100 000 cost could reduce total applications by ~20–25%.  
- **Technology and Finance adapt best; Consulting faces the most pressure.**

---

## 🏛️ Policy Interpretation

A single high fee affects sectors differently.  
Tech and finance firms can absorb higher costs or shift workers through OPT/CPT channels, while consulting firms—though large in volume—have fewer alternatives.  
Higher costs therefore **redirect** skilled labor rather than eliminate it.

---

## 🧩 Policy Recommendations

- **Tiered H-1B Fees:** Scale by firm size or wage level to keep smaller employers competitive.  
- **Extend STEM-OPT:** 36 → 48 months to give graduates more career stability.  
- **Support Consulting Firms:** Encourage university partnerships and cap-exempt options.  
- **Visa Transparency:** Require joint reporting of H-1B, OPT, and CPT data for future analysis.

---

## 🧠 Broader Takeaways

Raising H-1B fees doesn’t collapse demand—it reshapes it.  
The H-1B, OPT, and CPT programs act as a connected system where flexibility determines resilience.  
Understanding this interplay is key to maintaining U.S. innovation and global competitiveness.

---

## 🧾 Citation

> **Novith, Diyouva C.** (2024). *Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock.*  
> Carnegie Mellon University, Heinz College of Information Systems and Public Policy.

APA:
```
Novith, D. C. (2024). Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock.  
Carnegie Mellon University, Heinz College of Information Systems and Public Policy.
```

---

## ✨ Acknowledgment

Developed as part of a Final Project for the **Python Programming II – Data Analysis** course at  
**Carnegie Mellon University – Heinz College of Information Systems and Public Policy**.  
This project combines empirical data, simulation modeling, and open-source visualization  
to promote transparent, data-driven policymaking on international talent and immigration issues.