import matplotlib.pyplot as plt
import numpy as np
from analysis.helper import cut_off_record


def voltage_time(df_record):
    # Get data from each column
    record_data = df_record[["Cycle Count", "Voltage"]].to_numpy()

    # Cut off pre-cycles
    record_data = cut_off_record(record_data)

    # Get voltage data
    record_data = record_data[:, 1]

    # Create x-axis
    time_interval = 10  # seconds
    x = time_interval * np.arange(record_data.size)

    # Plotting
    plt.plot(
        x,
        record_data,
        color="b",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage vs. Time")
    plt.grid()
    plt.show()


def current_time(df_record):
    # Get data from each column
    record_data = df_record[["Cycle Count", "Current"]].to_numpy()

    # Cut off pre-cycles
    record_data = cut_off_record(record_data)

    # Get current data
    record_data = record_data[:, 1]

    # Create x-axis
    time_interval = 10  # seconds
    x = time_interval * np.arange(record_data.size)

    # Plotting
    plt.plot(
        x,
        record_data,
        color="b",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Current (mA)")
    plt.title("Current vs. Time")
    plt.grid()
    plt.show()
