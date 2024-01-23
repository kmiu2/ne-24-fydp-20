import matplotlib.pyplot as plt
import numpy as np
from helper import cut_off_record


def voltage_time(df):
    # Get data from each column
    charge_data = df[["Voltage", "Cycle Count"]].to_numpy()

    # Cut off pre-cycles
    charge_data = cut_off_record(charge_data)

    # Remove cycle count column
    charge_data = charge_data[:, 0]

    # Create x-axis
    time_interval = 10  # seconds
    x = time_interval * np.arange(charge_data.size)

    # Plotting
    plt.plot(
        x,
        charge_data,
        color="b",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage Over Cycle Life")
    plt.show()
