import os
import pandas as pd
from customer_requirements import print_customer_requirements
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
    "charge3_4.xlsx",
]

# Plotting
for d in data:
    path = "./data/" + d
    mass = 10.1e-6  # kg (meaning e-6 is milli)
    voltage = 2.5  # V

    print(f"\n---------- Reading Data: {d} ----------")
    print(f"Mass: {mass} kg")
    print(f"Voltage: {voltage} V")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")
    df_step = pd.read_excel(path, sheet_name="Step")

    # Customer Requirements
    print_customer_requirements(df_cycle, df_record, df_step, mass, voltage)

    # Plotting
    # voltage_time(df_record)
    # current_time(df_record)
    # discharge_capacity(df_cycle, mass, voltage)
    # columbic_efficiency(df_cycle)
    # capacity_voltage(df_step)
    # capacity_graph(df_record, mass)
