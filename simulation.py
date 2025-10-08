# simulation.py
import pandas as pd

def simulate_fee_change(df, alpha=0.1, elasticity=-0.3):
    """Simulate the effect of H1B fee changes by employer category."""
    df = df.copy()
    df["Simulated_Total_Applications"] = df["Total_Applications"] * (1 + elasticity * alpha)
    df["Simulated_Total_Approvals"] = df["Total_Approvals"] * (1 + elasticity * alpha)
    df["Change_%"] = 100 * (df["Simulated_Total_Applications"] / df["Total_Applications"] - 1)

    # Always keep grouping keys
    group_cols = [c for c in ["Year", "Fortune500", "Flexibility_Index"] if c in df.columns]
    if group_cols:
        summary = df.groupby(group_cols)[["Total_Applications", "Simulated_Total_Applications"]].sum().reset_index()
    else:
        summary = df[["Total_Applications", "Simulated_Total_Applications"]].sum().to_frame().T

    summary["Change_%"] = 100 * (
        summary["Simulated_Total_Applications"] / summary["Total_Applications"] - 1
    )

    return summary


if __name__ == "__main__":
    df = pd.read_csv("clean_h1b_data.csv")
    scenario = simulate_fee_change(df, alpha=0.2)  # +20% fee
    print(scenario)