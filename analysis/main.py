import os
import pandas as pd
from customer_requirements import print_customer_requirements
from chargeDischargeGraph import capacity_graph, capacity_voltage
from dischargeCapacityCyclingGraph import discharge_capacity
from coulombicEfficiencyGraph import columbic_efficiency
from voltageCurrentTimeGraph import voltage_time, current_time

# Ensure you are in the analysis directory
if os.getcwd().split("/")[-1] != "analysis":
    print("Please run this script from the analysis directory")
    exit()

# Data files
# Naming system: "life or charge" + "test suite" + "_" + "channel"
#                 + "(optional b and latter letters for continued testing)" + ".xlsx"
data = [
    "life3_4b.xlsx",
]

# Plotting
for d in data:
    path = "./data/" + d
    mass = 19.60  # mg
    mass *= 1e-6  # to kg
    voltage = 2.8  # V

    print(f"\n---------- Reading Data: {d} ----------")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")
    df_step = pd.read_excel(path, sheet_name="Step")

    print(f"Mass: {(mass * 1e6):.2f} mg")
    print(f"Voltage: {voltage} V")
    print(f"Number of data points: {len(df_record)}")
    print(f"Number of cycles: {len(df_cycle)}")

    # Customer Requirements
    print_customer_requirements(df_cycle, df_record, df_step, mass, voltage)

    # Plotting
    # voltage_time(df_record)
    # current_time(df_record)
    # discharge_capacity(df_cycle, mass, voltage)
    columbic_efficiency(df_cycle)
    # capacity_voltage(df_step)
    # capacity_graph(df_record, mass)
