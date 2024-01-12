import matplotlib.pyplot as plt
import numpy as np


def voltage_time(df):
    # Get data from each column
    charge_data = df[["Voltage"]].to_numpy()

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
