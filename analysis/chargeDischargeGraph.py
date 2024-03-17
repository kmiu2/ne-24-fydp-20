import numpy as np
import matplotlib.pyplot as plt
from analysis.helper import cut_off_record, cut_off_step


def capacity_graph(df_record, mass, helper_parameters, save_plots):
    # Get data from each column
    record_data = df_record[
        ["Cycle Count", "Capacity", "Voltage", "Step", "Step Mode"]
    ].to_numpy()

    # Cut off pre-cycles
    record_data = cut_off_record(record_data, helper_parameters)

    # Set variables
    num_data_points = len(record_data[:, 0])
    half_cycles = 0  # Can use cycle count for legend if need be - definitely looks cluttered with too many cycles
    cycle_data = np.zeros([1, 2])

    # Plotting
    plt.clf()
    plt.xlabel("Specific Capacity (mAh/kg)")
    plt.ylabel("Voltage (V)")
    plt.title("Charge/Discharge Cycles")
    plt.grid()

    # Loop through each data point
    for i in range(num_data_points - 1):
        current_cycle_type = record_data[i, 4]
        previous_cycle_type = record_data[i - 1, 4]

        # Get data for charge/discharge cycles
        if current_cycle_type == "CCD" or current_cycle_type == "CCC":
            # If the cycle type changed, update params
            if current_cycle_type != previous_cycle_type:
                half_cycles = half_cycles + 1
                cycle_data = np.zeros([1, 2])

            # Add the data point to the cycle data
            cycle_data = np.concatenate(
                (cycle_data, [[record_data[i, 1] / mass, record_data[i, 2]]])
            )

            # If it's the last data point of the cycle, plot the cycle
            if record_data[i + 1, 4] != current_cycle_type:
                plt.plot(cycle_data[1:, 0], cycle_data[1:, 1], color="#38761d")

    # Plotting
    if save_plots:
        plt.savefig("graphs/capacity_voltage.png", dpi=300, bbox_inches="tight")
    else:
        plt.show()


def capacity_voltage(df, helper_parameters, save_plots):
    # Get data from each column
    voltage_data = df[["Step", "Mode", "StartVolt", "EndVolt"]].to_numpy()

    # Cut off pre-cycles
    voltage_data = cut_off_step(voltage_data, helper_parameters)

    num_data_points = len(voltage_data[:, 0])
    lower_voltages = []
    upper_voltages = []

    # Loop through each data point
    for i in range(num_data_points):
        # Initial Rest Voltage
        if voltage_data[i, 0] == 1 and voltage_data[i, 1] == "Rest":
            upper_voltages.append(voltage_data[i, 2])
            lower_voltages.append(0)

        elif voltage_data[i, 1] == "CCD":
            upper_voltages.append(voltage_data[i, 3])
            lower_voltages.append(voltage_data[i, 2])

        elif voltage_data[i, 1] == "CCC":
            upper_voltages.append(voltage_data[i, 2])
            lower_voltages.append(voltage_data[i, 3])

    cycle_count = np.arange(1, (len(lower_voltages)) / 2 + 1, 0.5)

    # Plotting
    plt.clf()
    plt.plot(cycle_count, lower_voltages, color="blue")
    # plt.plot(cycle_count, upper_voltages, color="red")
    plt.xlabel("Cycle")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage vs. Cycle")
    plt.grid()
    if save_plots:
        plt.savefig("graphs/voltage_cycle.png", dpi=300, bbox_inches="tight")
    else:
        plt.show()
