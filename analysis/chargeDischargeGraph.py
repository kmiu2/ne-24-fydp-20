import numpy as np
import matplotlib.pyplot as plt

cm = plt.colormaps["hsv"]


def capacity_graph(df, mass):
    # Get data from each column
    charge_data = df[["Capacity", "Voltage", "Step", "Step Mode"]].to_numpy()

    # Set variables
    num_data_points = len(charge_data[:, 0])
    cycle_count = 0  # Can use cycle count for legend if need be - definitely looks cluttered with too many cycles
    cycle_data = np.zeros([1, 2])

    # Subplots for linear and log scale
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    fig.suptitle("Charge/Discharge Cycles")
    ax[0].set_xlabel("Specific Capacity (mAh/g)")
    ax[0].set_ylabel("Voltage (V)")
    ax[1].set_xlabel("Specific Capacity (mAh/g)")
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
                cycle_count = cycle_count + 1
                cycle_data = np.zeros([1, 2])

            # Add the data point to the cycle data
            cycle_data = np.concatenate(
                (cycle_data, [[charge_data[i, 0] / mass, charge_data[i, 1]]])
            )

            # If it's the last data point of the cycle, plot the cycle
            if charge_data[i + 1, 3] != current_cycle_type:
                ax[0].plot(cycle_data[1:, 0], cycle_data[1:, 1], color=cm(cycle_count))
                ax[1].plot(cycle_data[1:, 0], cycle_data[1:, 1], color=cm(cycle_count))

    # Print data
    print("Cycle Count: ", cycle_count)

    # Plotting
    plt.show()
