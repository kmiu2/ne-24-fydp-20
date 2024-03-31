################### Parameters to Edit ###################
# Data files Naming system: "cell number"_"life or charge"_ + "(optional letters for further tests)".xlsx
# Ex: 18_life.xlsx, 42_life.xlsx
# Put mass in mg

data = [
    {
        "file_name": "51_life.xlsx",
        "mass_mg": 14.2,
        "is_anode": False,
        "color": "#38761d",
        "label": "Cathode",
    },
]  # Data is an array, which means you can put run multiple data files in one go
custom_voltage = 0  # Set voltages to be 3 for anodes

show_plots = True
save_plots = True
num_pre_cycles = 0  # Number of precycles to remove from start

#################################################s
################### Main Code ###################
default_helper_parameters = {
    "remove_from_start": 1,  # Removes last incomplete cycle
    "remove_from_end": 1,  # Removes first incomplete cycle
    "num_lifetime_cycles": 1000,
    "custom_range": False,  # If True, will use custom_start and custom_num_cycles
    "custom_start": 3,  # Starting at cycle N
    "custom_num_cycles": 2,  # Number of cycles to include
}

helper_parameters = default_helper_parameters
helper_parameters["remove_from_start"] = (
    helper_parameters["remove_from_start"] + num_pre_cycles
)

import pandas as pd
from analysis.customer_requirements import print_customer_requirements
from analysis.chargeDischargeGraph import capacity_graph, capacity_voltage
from analysis.dischargeCapacityCyclingGraph import discharge_capacity
from analysis.coulombicEfficiencyGraph import columbic_efficiency
from analysis.voltageCurrentTimeGraph import voltage_time, current_time

# Plotting
for d in data:
    path = "./data/" + d["file_name"]
    is_anode = d["is_anode"]
    if is_anode:
        custom_voltage = 3  # Set voltages for anodes

    print(f"\n---------- Reading Data: {d['file_name']} ----------")

    # Read data from excel file
    df_record = pd.read_excel(path, sheet_name="Record")
    df_cycle = pd.read_excel(path, sheet_name="Cycle")
    df_step = pd.read_excel(path, sheet_name="Step")

    # Get mass and max voltage
    mass_kg = 1e-6 * d["mass_mg"]  # kg
    record_data = df_record[["Voltage"]].to_numpy()
    max_voltage = 0
    if custom_voltage != 0:
        max_voltage = custom_voltage
    else:
        max_voltage = record_data.max()

    print(f"Mass: {(mass_kg * 1e6):.2f} mg")
    print(f"Voltage: {max_voltage:.2f} V")
    print(f"Number of cycles that ran: {len(df_cycle)}")

    # Customer Requirements
    print_customer_requirements(
        is_anode, df_cycle, df_record, df_step, mass_kg, max_voltage, helper_parameters
    )

    # Plotting
    if show_plots:
        voltage_time(df_record, helper_parameters, save_plots, label=d["label"])
        discharge_capacity(
            is_anode,
            df_cycle,
            df_record,
            mass_kg,
            max_voltage,
            helper_parameters,
            save_plots,
            label=d["label"],
        )
        columbic_efficiency(df_cycle, helper_parameters, save_plots, label=d["label"])
        capacity_voltage(df_step, helper_parameters, save_plots, label=d["label"])
        current_time(df_record, helper_parameters, save_plots, label=d["label"])
        capacity_graph(
            df_record,
            mass_kg,
            helper_parameters,
            save_plots,
            label=d["label"],
        )

    print("------------------------------")
