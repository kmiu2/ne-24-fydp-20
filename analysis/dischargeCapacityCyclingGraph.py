# Plot discharge capacity as a function of cycle number - check units!
# Need to figure out how to get specific capacity as well
import matplotlib.pyplot as plt
import numpy as np
from helper import cut_off_cycle


def discharge_capacity(df, mass, voltage):
    # Get data from each column
    charge_data = df[["Cycle", "CapD"]].to_numpy()

    # Cut off pre-cycles
    charge_data = cut_off_cycle(charge_data)

    # (mAh)*(V)/1000 = (Wh)
    wh_data = charge_data[:, 1] * voltage / 1000
    x = charge_data[:, 0]
    y = wh_data / mass
    polyfit = np.polyfit(x, y, 15)

    # Plotting
    plt.plot(
        x,
        y,
        linestyle="None",
        marker="o",
        color="lightskyblue",
    )
    plt.plot(
        x,
        np.polyval(polyfit, x),
        color="b",
    )
    plt.xlabel("Cycle Number")
    plt.ylabel("Specific Discharge Capacity (Wh/kg)")
    plt.title("Capacity Over Cycle Life")
    plt.show()
