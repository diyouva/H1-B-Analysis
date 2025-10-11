import pandas as pd

# ----------------------------------------------------------------------
# 1. Simulation Core Function
# ----------------------------------------------------------------------
# def simulate_fee_change(df, alpha=0.1, elasticity=-0.3):
#     """
#     Simulate the response of employers to changes in H-1B filing fees.

#     Parameters
#     ----------
#     df : pandas.DataFrame
#         Cleaned and integrated dataset from prepare.py.
#     alpha : float
#         Fee change in proportional terms (e.g., 0.2 = +20 % increase).
#     elasticity : float
#         Sensitivity of application volume to fee change.

#     Returns
#     -------
#     summary : pandas.DataFrame
#         Aggregated results showing baseline and simulated applications by category and year.
#     """
#     df = df.copy()
#     df["Simulated_Total_Applications"] = df["Total_Applications"] * (1 + elasticity * alpha)
#     df["Simulated_Total_Approvals"] = df["Total_Approvals"] * (1 + elasticity * alpha)
#     df["Change_%"] = 100 * (df["Simulated_Total_Applications"] / df["Total_Applications"] - 1)

#     group_cols = [c for c in ["Year", "Fortune500", "Flexibility_Index"] if c in df.columns]
#     summary = df.groupby(group_cols)[["Total_Applications", "Simulated_Total_Applications"]].sum().reset_index()
#     summary["Change_%"] = 100 * (
#         summary["Simulated_Total_Applications"] / summary["Total_Applications"] - 1
#     )

#     print("Simulation completed. Returning aggregated summary DataFrame.")
#     return summary

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


# # ----------------------------------------------------------------------
# # 2. Stand-alone Execution Example
# # ----------------------------------------------------------------------
# if __name__ == "__main__":
#     df = pd.read_csv("clean_h1b_data.csv")
#     result = simulate_fee_change(df, alpha=0.2, elasticity=-0.3)
#     result.to_csv("simulation_result.csv", index=False)
#     print("simulation_result.csv successfully saved.")