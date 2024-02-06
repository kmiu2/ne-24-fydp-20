import os
import pandas as pd
from chargeDischargeGraph import capacity_graph, capacity_voltage
from dischargeCapacityCyclingGraph import discharge_capacity
from columbicEfficiencyGraph import columbic_efficiency
from voltageCurrentTimeGraph import voltage_time, current_time

# Ensure you are in the analysis directory
if os.getcwd().split("/")[-1] != "analysis":
    print("Please run this script from the analysis directory")
    exit()

# Data files
data = [
    "charge2_7b.xlsx",
]

# Plotting
for d in data:
    path = "./data/" + d
    mass = 10.1e-6  # kg (meaning e-6 is milli)
    voltage = 2.5  # V

    print(f"\n---------- Reading Data: {d} ----------")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")
    df_step = pd.read_excel(path, sheet_name="Step")

    # Plotting
    voltage_time(df_record)
    current_time(df_record)
    discharge_capacity(df_cycle, mass, voltage)
    columbic_efficiency(df_cycle)
    capacity_voltage(df_step)
    capacity_graph(df_record, mass)
