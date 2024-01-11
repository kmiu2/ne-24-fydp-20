# Script to import cell data from Excel and graph charge/discharge curves for each cycle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def capacity_graph(path, sheetname, mass):
    df = pd.read_excel(path, sheet_name=sheetname)

    charge_data = df[["Capacity", "Voltage", "Step", "Step Mode"]].to_numpy()

    num_data_points = len(charge_data[:, 0])
    cycle_count = 0  # Can use cycle count for legend if need be - definitely looks cluttered with too many cycles
    current_cycle_type = "Rest"

    for i in range(0, num_data_points):
        if charge_data[i, 3] == "Rest" and current_cycle_type != "Rest":
            current_cycle_type = "Rest"

        elif charge_data[i, 3] == "CCD":
            if current_cycle_type != "CCD":
                cycle_count = cycle_count + 1
                current_cycle_type = "CCD"
                cycle_data = np.zeros([1, 2])

            cycle_data = np.concatenate(
                (cycle_data, [[charge_data[i, 0] / mass, charge_data[i, 1]]])
            )

            if i < num_data_points - 1 and charge_data[i + 1, 3] != current_cycle_type:
                plt.plot(cycle_data[1:, 0], cycle_data[1:, 1])

        elif charge_data[i, 3] == "CCC":
            if current_cycle_type != "CCC":
                current_cycle_type = "CCC"
                cycle_data = np.zeros([1, 2])

            cycle_data = np.concatenate(
                (cycle_data, [[charge_data[i, 0] / mass, charge_data[i, 1]]])
            )

            if i < num_data_points - 1 and charge_data[i + 1, 3] != current_cycle_type:
                plt.plot(cycle_data[1:, 0], cycle_data[1:, 1])

    plt.title("Charge/discharge Cycles")
    plt.xlabel("Specific Capacity (mAh/g)")
    plt.ylabel("Voltage (V)")
    plt.show()
