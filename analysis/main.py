import os
import pandas as pd
from chargeDischargeGraph import capacity_graph, capacity_voltage
from dischargeCapacityCyclingGraph import discharge_capacity
from columbicEfficiencyGraph import columbic_efficiency
from voltageTimeGraph import voltage_time

# Ensure you are in the analysis directory
if os.getcwd().split("/")[-1] != "analysis":
    print("Please run this script from the analysis directory")
    exit()

# Data files
data = [
    "life1_5.xlsx",
]

# Plotting
for d in data:
    path = "./data/" + d
    mass = 6e-6  # kg

    print(f"\n---------- Reading Data: {d} ----------")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")
    df_step = pd.read_excel(path, sheet_name="Step")

    # Plotting
    capacity_voltage(df_step)
    capacity_graph(df_record, mass)
    voltage_time(df_record)
    discharge_capacity(df_cycle, mass)
    columbic_efficiency(df_cycle)
