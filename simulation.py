# simulation.py
import pandas as pd

def simulate_fee_change(df, alpha=0.1, elasticity=-0.3):
    """
    Simulate the effect of H1B fee change on application volume.
    alpha: percentage change in fee (+0.1 for +10%, -0.1 for -10%)
    elasticity: responsiveness of applications to fee change
    """
    df = df.copy()
    df["Simulated_Total_Applications"] = df["Total_Applications"] * (1 + elasticity * alpha)
    df["Simulated_Total_Approvals"] = df["Total_Approvals"] * (1 + elasticity * alpha)
    df["Change_%"] = 100 * (df["Simulated_Total_Applications"] / df["Total_Applications"] - 1)

    summary = df.groupby("Year")[["Total_Applications", "Simulated_Total_Applications"]].sum()
    summary["Change_%"] = 100 * (summary["Simulated_Total_Applications"] / summary["Total_Applications"] - 1)
    return summary


if __name__ == "__main__":
    df = pd.read_csv("clean_h1b_data.csv")
    scenario = simulate_fee_change(df, alpha=0.2)  # +20% fee
    print(scenario)