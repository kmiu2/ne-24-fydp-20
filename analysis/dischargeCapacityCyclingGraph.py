# Plot discharge capacity as a function of cycle number - check units!
# Need to figure out how to get specific capacity as well
import matplotlib.pyplot as plt


def discharge_capacity(df, mass):
    # Get data from each column
    charge_data = df[["Cycle", "CapD"]].to_numpy()

    # Plotting
    plt.plot(
        charge_data[:, 0],
        charge_data[:, 1] / mass,
        linestyle="-",
        marker="o",
        color="b",
    )
    plt.xlabel("Cycle Number")
    plt.ylabel("Specific Discharge Capacity (mAh/g)")
    plt.title("Capacity Over Cycle Life")
    plt.show()
