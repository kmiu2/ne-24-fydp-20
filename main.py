################### Parameters to Edit ###################
# Data files Naming system: "cell number"_"life or charge"_ + "(optional letters for further tests)".xlsx
# Ex: 18_life.xlsx, 42_life.xlsx
# Put mass in mg

data = [
    {
        "file_name": "51_life_pre.xlsx",
        "mass_mg": 20.00,
    }
]  # Data is an array, which means you can put run multiple data files in one go
show_plots = True
custom_voltage = 0  # Set a different voltage. If 0, it will take 95% of max voltage

#################################################
################### Main Code ###################
import pandas as pd
from analysis.customer_requirements import print_customer_requirements
from analysis.chargeDischargeGraph import capacity_graph, capacity_voltage
from analysis.dischargeCapacityCyclingGraph import discharge_capacity
from analysis.coulombicEfficiencyGraph import columbic_efficiency
from analysis.voltageCurrentTimeGraph import voltage_time, current_time

# Plotting
for d in data:
    path = "./data/" + d["file_name"]

    print(f"\n---------- Reading Data: {d['file_name']} ----------")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")
    df_step = pd.read_excel(path, sheet_name="Step")

    # Get mass and max voltage
    # - Take 90% of the max voltage
    mass_kg = 1e-6 * d["mass_mg"]  # kg
    record_data = df_record[["Voltage"]].to_numpy()
    max_voltage = 0
    if custom_voltage != 0:
        max_voltage = custom_voltage
    else:
        max_voltage = record_data.max() * 0.95

    print(f"Mass: {(mass_kg * 1e6):.2f} mg")
    print(f"Voltage: {max_voltage:.2f} V")
    print(f"Number of cycles that ran: {len(df_cycle)}")

    # Customer Requirements
    print_customer_requirements(df_cycle, df_record, df_step, mass_kg, max_voltage)

    # Plotting
    if show_plots:
        voltage_time(df_record)
        capacity_voltage(df_step)
        current_time(df_record)
        discharge_capacity(df_cycle, mass_kg, max_voltage)
        columbic_efficiency(df_cycle)
        # capacity_graph(df_record, mass)

    print("------------------------------")
