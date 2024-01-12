import os
import pandas as pd
from chargeDischargeGraph import capacity_graph
from dischargeCapacityCyclingGraph import discharge_capacity
from columbicEfficiencyGraph import columbic_efficiency
from voltageTimeGraph import voltage_time

# Ensure you are in the analysis directory
if os.getcwd().split("/")[-1] != "analysis":
    print("Please run this script from the analysis directory")
    exit()

# Data files
data = [
    "003_7(--).xlsx",
    "003_8(--).xlsx",
]

# Plotting
for d in data:
    path = "./data/" + d
    mass = 6e-3  # g

    print(f"\n---------- Reading Data: {d} ----------")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")

    # Plotting
    capacity_graph(df_record, mass)
    voltage_time(df_record)
    discharge_capacity(df_cycle, mass)
    columbic_efficiency(df_cycle)
