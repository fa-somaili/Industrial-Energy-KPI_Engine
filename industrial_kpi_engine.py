import numpy as np
import pandas as pd

# 1. Simulate 30 days of hourly industrial data
np.random.seed(42)
time_index = pd.date_range(start="2026-09-01", periods=24 * 30, freq="h")

# Production output in Tons (Copper / Steel batch)
production_tons = np.random.uniform(15, 35, size=len(time_index))

# Electricity consumption in kWh (with base load + production scaling)
electricity_kwh = production_tons * 120 + np.random.normal(
    500, 50, size=len(time_index)
)

# Natural Gas consumption in m³
gas_m3 = production_tons * 15 + np.random.normal(50, 10, size=len(time_index))

# Combine into a DataFrame
df_raw = pd.DataFrame(
    {
        "Timestamp": time_index,
        "Production_Tons": np.round(production_tons, 2),
        "Electricity_kWh": np.round(electricity_kwh, 2),
        "Gas_m3": np.round(gas_m3, 2),
    }
)

# Save raw dataset to CSV
df_raw.to_csv("industrial_energy_data.csv", index=False)
print("Success: Generated 'industrial_energy_data.csv' with 720 hourly records!")

# 2. Load and Analyze Industrial KPIs
df = pd.read_csv("industrial_energy_data.csv")

# Calculate Specific Energy Consumption (SEC) per ton of output
# SEC = Energy consumed divided by production output (kWh/Ton and m3/Ton)
df["SEC_Electricity_kWh_Ton"] = df["Electricity_kWh"] / df["Production_Tons"]
df["SEC_Gas_m3_Ton"] = df["Gas_m3"] / df["Production_Tons"]

# Estimate Carbon Emissions (approx. factors: 0.4 kg CO2/kWh for electricity, 2.0 kg CO2/m3 for gas)
df["CO2_Electricity_kg"] = df["Electricity_kWh"] * 0.4
df["CO2_Gas_kg"] = df["Gas_m3"] * 2.0
df["Total_CO2_kg"] = df["CO2_Electricity_kg"] + df["CO2_Gas_kg"]

# Create a Daily Summary Aggregation for Management
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Date"] = df["Timestamp"].dt.date

daily_kpi = (
    df.groupby("Date")
    .agg(
        {
            "Production_Tons": "sum",
            "Electricity_kWh": "sum",
            "Gas_m3": "sum",
            "Total_CO2_kg": "sum",
        }
    )
           .reset_index()
)

# Calculate Daily SEC
daily_kpi["Daily_SEC_Electricity"] = (
    daily_kpi["Electricity_kWh"] / daily_kpi["Production_Tons"]
)
daily_kpi["Daily_SEC_Gas"] = daily_kpi["Gas_m3"] / daily_kpi["Production_Tons"]

# Export to a professional summary Excel file
output_kpi_file = "Industrial_Energy_KPI_Report.xlsx"
daily_kpi.to_excel(output_kpi_file, index=False)

print(
    f"Success: Industrial KPI Engine executed! Summary report saved to '{output_kpi_file}'."
)


    