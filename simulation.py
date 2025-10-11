import pandas as pd
import numpy as np

# ----------------------------------------------------------------------
# Simulation with Heterogeneous Elasticity
# ----------------------------------------------------------------------
def simulate_fee_change(df, alpha=0.1, elasticity_low=-0.5, elasticity_high=-0.2):
    """
    Simulate the response of employers to changes in H-1B filing fees,
    with heterogeneous elasticity by flexibility level.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned and integrated dataset from prepare.py.
    alpha : float
        Fee change in proportional terms (e.g., 0.2 = +20% increase).
    elasticity_low : float
        Elasticity for less flexible employers.
    elasticity_high : float
        Elasticity for more flexible employers.

    Returns
    -------
    summary : pandas.DataFrame
        Aggregated results showing baseline and simulated applications by flexibility and year.
    """

    df = df.copy()

    # --- Step 1: Discretize flexibility ---
    if "Flexibility_Index" in df.columns:
        df["Flex_Group"] = np.where(df["Flexibility_Index"] > 0.5, "More Flexible", "Less Flexible")
    else:
        raise ValueError("Column 'Flexibility_Index' is missing from dataframe.")

    # --- Step 2: Assign elasticity per group ---
    df["Elasticity"] = np.where(df["Flex_Group"] == "More Flexible", elasticity_high, elasticity_low)

    # --- Step 3: Apply elasticity to simulate response ---
    df["Simulated_Total_Applications"] = df["Total_Applications"] * (1 + df["Elasticity"] * alpha)
    df["Change_%"] = 100 * (df["Simulated_Total_Applications"] / df["Total_Applications"] - 1)

    # --- Step 4: Aggregate results by Year & Flexibility Group ---
    group_cols = [c for c in ["Year", "Flex_Group"] if c in df.columns]
    summary = (
        df.groupby(group_cols, as_index=False)[["Total_Applications", "Simulated_Total_Applications"]]
          .sum()
    )
    summary["Change_%"] = 100 * (summary["Simulated_Total_Applications"] / summary["Total_Applications"] - 1)

    print("Simulation completed with heterogeneous elasticity:")
    print(f"  Less Flexible  → ε = {elasticity_low}")
    print(f"  More Flexible  → ε = {elasticity_high}")
    return summary