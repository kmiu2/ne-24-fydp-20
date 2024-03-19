import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from helper import cut_off_cycle, cut_off_record
from scipy.integrate import simpson

data = [
    {
        "file_name": "51_life.xlsx",
        "mass_mg": 1.865,
        "is_anode": True,
        "color": "#38761d",
        "label": "Anode",
    },
    {
        "file_name": "69_life.xlsx",
        "mass_mg": 13.44,
        "is_anode": False,
        "color": "#7CA5B8",
        "label": "Cathode",
    },
]
custom_voltage = 0  # Set voltages to be 3 for anodes
show_plots = True
save_plots = True
num_pre_cycles = 0  # Number of precycles to remove from start

#################################################
################### Main Code ###################
default_helper_parameters = {
    "remove_from_start": 1,  # Removes last incomplete cycle
    "remove_from_end": 1,  # Removes first incomplete cycle
    "num_lifetime_cycles": 1000,
    "custom_range": False,  # If True, will use custom_start and custom_num_cycles
    "custom_start": 2,  # Starting at cycle N
    "custom_num_cycles": 1,  # Number of cycles to include
}

helper_parameters = default_helper_parameters
helper_parameters["remove_from_start"] = (
    helper_parameters["remove_from_start"] + num_pre_cycles
)

plt.clf()
plt.figure()

# Plotting
for d in data:
    path = "./data/" + d["file_name"]
    is_anode = d["is_anode"]

    if is_anode:
        custom_voltage = 3  # Set voltages for anodes
        helper_parameters["custom_range"] = True
        helper_parameters["custom_start"] = 0
        helper_parameters["custom_num_cycles"] = 4
    else:
        helper_parameters["custom_range"] = False

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

    voltage = max_voltage
    mass = mass_kg

    # Get data from each column
    cycle_data = df_cycle[["Cycle", "CapC", "CapD"]].to_numpy()
    record_data = df_record[
        ["Cycle Count", "Current", "Voltage", "Step", "Step Mode"]
    ].to_numpy()

    # Cut off pre-cycles
    cycle_data = cut_off_cycle(cycle_data, helper_parameters)
    record_data = cut_off_record(record_data, helper_parameters)

    if is_anode:
        wh_cycle_data = np.array(cycle_data[:, 1]) * voltage / 1000
        x = cycle_data[:, 0]
        y = wh_cycle_data / mass
    else:
        cycle_indices = []
        for i in range(1, len(record_data)):
            if record_data[i][4] == "Rest" or record_data[i - 1][4] == "Rest":
                continue
            if record_data[i][4] != record_data[i - 1][4]:
                cycle_indices.append(i)

        energies = []
        for i in range(len(cycle_indices) - 1):
            start = cycle_indices[i]
            end = cycle_indices[i + 1]
            cycle_current = record_data[start:end, 1]  # mA
            cycle_current = cycle_current / 1000  # A
            cycle_voltage = record_data[start:end, 2]  # V
            time_interval = 10  # seconds
            time = time_interval * np.arange(cycle_current.size)
            time = time / 3600  # hours
            energy = simpson(abs(cycle_current * cycle_voltage), time)  # Wh
            energies.append(energy)

        discharge_energy_densities = []
        for i in range(0, len(energies) - 1, 2):
            energy_ccd = energies[i + 1]
            discharge_energy_density = energy_ccd / mass
            discharge_energy_densities.append(discharge_energy_density)

        x = cycle_data[:, 0]
        y = discharge_energy_densities

    # Cut off the last extra x element if len(x) > len(y)
    if len(x) > len(y):
        x = x[: len(y)]

    # Plotting
    plt.plot(
        x,
        y,
        linestyle="-",
        marker="o",
        color=d["color"],
        label=d["label"],
    )

plt.xlabel("Cycle Number")
plt.ylabel("Gravimetric Energy Density (Wh/kg_electrode)")
plt.title("Capacity vs. Cycles")
plt.grid()
plt.legend()

if save_plots:
    plt.savefig(
        "graphs/multi_discharge_capacity.png",
        dpi=300,
        bbox_inches="tight",
        transparent=False,
    )
else:
    plt.show()
