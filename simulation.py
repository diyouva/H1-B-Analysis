# simulation.py
"""
SIMULATION.PY
Fee elasticity simulation for:
"Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock"

Author: Diyouva C. Novith
Carnegie Mellon University, Heinz College of Information Systems and Public Policy

Purpose:
Estimate how H-1B applications respond to a fee shock and how firms with different flexibility levels
(adapted through OPT and CPT) redistribute demand across employment categories.

Economic rationale:
    ΔApplications / Applications = Elasticity × ΔFee
A higher fee leads to proportionally fewer applications, with adaptive substitution among flexible firms.
"""

import pandas as pd

# ----------------------------------------------------------------------
# 1. Simulation Core Function
# ----------------------------------------------------------------------
def simulate_fee_change(df, alpha=0.1, elasticity=-0.3):
    """
    Simulate the response of employers to changes in H-1B filing fees.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned and integrated dataset from prepare.py.
    alpha : float
        Fee change in proportional terms (e.g., 0.2 = +20 % increase).
    elasticity : float
        Sensitivity of application volume to fee change.

    Returns
    -------
    summary : pandas.DataFrame
        Aggregated results showing baseline and simulated applications by category and year.
    """
    df = df.copy()
    df["Simulated_Total_Applications"] = df["Total_Applications"] * (1 + elasticity * alpha)
    df["Simulated_Total_Approvals"] = df["Total_Approvals"] * (1 + elasticity * alpha)
    df["Change_%"] = 100 * (df["Simulated_Total_Applications"] / df["Total_Applications"] - 1)

    group_cols = [c for c in ["Year", "Fortune500", "Flexibility_Index"] if c in df.columns]
    summary = df.groupby(group_cols)[["Total_Applications", "Simulated_Total_Applications"]].sum().reset_index()
    summary["Change_%"] = 100 * (
        summary["Simulated_Total_Applications"] / summary["Total_Applications"] - 1
    )

    print("Simulation completed. Returning aggregated summary DataFrame.")
    return summary


# ----------------------------------------------------------------------
# 2. Stand-alone Execution Example
# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv("clean_h1b_data.csv")
    result = simulate_fee_change(df, alpha=0.2, elasticity=-0.3)
    result.to_csv("simulation_result.csv", index=False)
    print("simulation_result.csv successfully saved.")