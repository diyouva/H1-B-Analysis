# 🎓 Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock

**Author:** Diyouva C. Novith  
*Carnegie Mellon University — Heinz College of Information Systems and Public Policy*  
📄 [Policy Brief (PDF)](./policy_brief/Policy%20Brief.pdf)

---

## 🧩 Overview

This project models how a proposed **USD 100 000 H-1B visa filing fee** could reshape U.S. post-study employment for international graduates.  
By combining official **USCIS H-1B DataHub** records (2015–2023) with scraped employer lists for **OPT** (Optional Practical Training) and **CPT** (Curricular Practical Training), the study quantifies how employers adapt hiring behavior under cost pressure.

The repository implements a transparent **paper-with-code** workflow:

| Stage | Script | Purpose |
|-------|---------|----------|
| 🧹 **Data Preparation** | [`prepare.py`](./prepare.py) | Clean and merge all datasets; generate EDA plots |
| 📈 **Elasticity Simulation** | [`simulation.py`](./simulation.py) | Estimate behavioral response to fee changes |
| 🌐 **Interactive Dashboard** | [`app.py`](./app.py) | Visualize results with Streamlit |

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Prepare Data
```bash
python prepare.py
```
This step:
- Loads and standardizes H-1B, OPT, and CPT data  
- Produces `/data/clean_h1b_data.csv`  
- Exports charts to `/eda/`

### 3️⃣ Launch Dashboard
```bash
streamlit run app.py
```

### 4️⃣ (Optional) Refresh Employer Lists
```bash
python opt_company.py
python cpt_company.py
```

---

## 🗂️ Repository Structure
```
project/
├── data/
│   ├── h1b_datahubexport-2015.csv … 2023.csv
│   ├── fortune500_opt_companies_2024.csv
│   ├── cpt_employers_day1cptuniversities_bs4.csv
│   └── clean_h1b_data.csv
│
├── eda/
│   ├── h1b_approvals_trend.png
│   └── fortune500_comparison.png
│
├── policy_brief/
│   └── Policy Brief.pdf
│
├── app.py
├── cpt_company.py
├── opt_company.py
├── prepare.py
├── simulation.py
├── requirements.txt
└── README.md
```

---

## 📊 Data Sources

| Dataset | Description | Source |
|----------|--------------|--------|
| **USCIS H-1B DataHub (2015–2023)** | Petition approvals & denials | [USCIS Data Hub](https://www.uscis.gov/) |
| **UnitedOPT Employer List (2024)** | OPT-friendly employers (Fortune 500) | [UnitedOPT](https://unitedopt.com/) |
| **Day-1 CPT University Employer List** | CPT-friendly employers | [Day1CPT](https://day1cpt.org/) |

**Derived Outputs**
- `/data/clean_h1b_data.csv` — unified dataset  
- `/eda/*.png` — EDA charts for visualization  

---

## 🧮 Methodology

### Data Integration
All datasets are harmonized through automated preprocessing in `prepare.py`.  
Employer names are standardized, numeric fields validated, and categorical flags created:
```python
df["Flexibility_Index"] = df[["OPT_friendly", "CPT_friendly"]].sum(axis=1)
```
This index measures each employer’s adaptability across pathways.

### Simulation Model
Based on elasticity theory:
\[
\frac{\Delta A}{A} = \varepsilon \times \frac{\Delta F}{F}
\]
where  
- \( A \): Application volume  
- \( F \): Filing fee  
- \( \varepsilon \): Elasticity (≈ −0.3 baseline)

Implemented in `simulation.py`:
```python
df["Simulated_Total_Applications"] = df["Total_Applications"] * (1 + elasticity * alpha)
```

Employers with higher *Flexibility Index* experience smaller declines when fees increase.

---

## 📈 Findings

- H-1B demand remains high but adjusts structurally when costs rise.  
- A USD 100 000 filing fee causes ~ 20 % fewer applications.  
- Tech, finance, and consulting employers reallocate demand to OPT/CPT.  
- Employment shifts, not collapses — flexibility sustains innovation.

---

## 🏛️ Policy Recommendations

| Recommendation | Goal |
|----------------|------|
| **Tiered H-1B Fees** | Preserve competitiveness for SMEs |
| **Extend STEM-OPT (36→48 mo)** | Smooth transitions across visa cycles |
| **Expand Cap-Exempt Categories** | Support universities & research institutions |

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

## 🧩 License
Released under the **MIT License** — free to use, modify, and distribute with attribution.

---

## ✨ Acknowledgments
Developed as part of a policy analytics project at **Carnegie Mellon University’s Heinz College**.  
The project integrates empirical data, simulation modeling, and open-source visualization to advance data-driven immigration policy research.
