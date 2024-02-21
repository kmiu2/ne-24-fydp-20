import numpy as np
import matplotlib.pyplot as plt
from helper import cut_off_record, cut_off_step

cm = plt.colormaps["hsv"]


def capacity_graph(df, mass):
    # Get data from each column
    charge_data = df[
        ["Capacity", "Voltage", "Step", "Step Mode", "Cycle Count"]
    ].to_numpy()

    # Cut off pre-cycles
    charge_data = cut_off_record(charge_data)

    # Set variables
    num_data_points = len(charge_data[:, 0])
    half_cycles = 0  # Can use cycle count for legend if need be - definitely looks cluttered with too many cycles
    cycle_data = np.zeros([1, 2])

    # Subplots for linear and log scale
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    fig.suptitle("Charge/Discharge Cycles")
    ax[0].set_xlabel("Specific Capacity (mAh/kg)")
    ax[0].set_ylabel("Voltage (V)")
    ax[1].set_xlabel("Specific Capacity (mAh/kg)")
    ax[1].set_ylabel("Voltage (V)")
    ax[1].set_xscale("log")

    # Loop through each data point
    for i in range(num_data_points - 1):
        current_cycle_type = charge_data[i, 3]
        previous_cycle_type = charge_data[i - 1, 3]

        # Get data for charge/discharge cycles
        if current_cycle_type == "CCD" or current_cycle_type == "CCC":
            # If the cycle type changed, update params
            if current_cycle_type != previous_cycle_type:
                half_cycles = half_cycles + 1
                cycle_data = np.zeros([1, 2])

            # Add the data point to the cycle data
            cycle_data = np.concatenate(
                (cycle_data, [[charge_data[i, 0] / mass, charge_data[i, 1]]])
            )

            # If it's the last data point of the cycle, plot the cycle
            if charge_data[i + 1, 3] != current_cycle_type:
                ax[0].plot(cycle_data[1:, 0], cycle_data[1:, 1], color=cm(half_cycles))
                ax[1].plot(cycle_data[1:, 0], cycle_data[1:, 1], color=cm(half_cycles))

    print("Cycle count: " + str(half_cycles / 2))
    plt.grid()

    # Plotting
    plt.show()


def capacity_voltage(df):
    # Get data from each column
    voltage_data = df[["Step", "Mode", "StartVolt", "EndVolt"]].to_numpy()

    # Cut off pre-cycles
    voltage_data = cut_off_step(voltage_data, remove_one=True)

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
    plt.plot(cycle_count, lower_voltages, color="blue")
    # plt.plot(cycle_count, upper_voltages, color="red")
    plt.xlabel("Cycle")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage vs. Cycle")
    plt.grid()
    plt.show()
