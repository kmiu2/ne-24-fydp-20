import pandas as pd
from analysis.customer_requirements import print_customer_requirements
from analysis.chargeDischargeGraph import capacity_graph, capacity_voltage
from analysis.dischargeCapacityCyclingGraph import discharge_capacity
from analysis.coulombicEfficiencyGraph import columbic_efficiency
from analysis.voltageCurrentTimeGraph import voltage_time, current_time

# Data files
# Naming system: "cell number"_"life or charge"_ +
#                "(optional letters for further tests)".xlsx
data = [
    "42_life.xlsx",
]

# Plotting
for d in data:
    path = "./data/" + d
    mass = 30.10  # mg
    mass *= 1e-6  # to kg
    voltage = 2.0  # V

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
    voltage_time(df_record)
    capacity_voltage(df_step)
    current_time(df_record)
    discharge_capacity(df_cycle, mass, voltage)
    columbic_efficiency(df_cycle)
    capacity_graph(df_record, mass)
