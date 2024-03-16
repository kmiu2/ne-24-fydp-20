# Plot discharge capacity as a function of cycle number - check units!
# Need to figure out how to get specific capacity as well
import matplotlib.pyplot as plt
import numpy as np
from analysis.helper import cut_off_cycle


def discharge_capacity(df_cycle, mass, voltage):
    # Get data from each column
    cycle_data = df_cycle[["Cycle", "CapC", "CapD"]].to_numpy()

    # Cut off pre-cycles
    cycle_data = cut_off_cycle(cycle_data)

    # (mAh)*(V)/1000 = (Wh)
    # Get the larger of CapC and CapD
    capacities = []
    for cycle in cycle_data:
        capacities.append(max(cycle[1], cycle[2]))

    wh_cycle_data = np.array(capacities) * voltage / 1000
    x = cycle_data[:, 0]
    y = wh_cycle_data / mass

    # Plotting
    plt.plot(
        x,
        y,
        linestyle="-",
        marker="o",
        color="b",
    )
    plt.xlabel("Cycle Number")
    plt.ylabel("Specific Discharge Capacity (Wh/kg)")
    plt.title("Capacity vs. Cycles")
    plt.grid()
    plt.show()
