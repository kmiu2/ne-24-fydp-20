# Plot discharge capacity as a function of cycle number - check units!
# Need to figure out how to get specific capacity as well

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def discharge_capacity(path, sheetname, mass):
    df = pd.read_excel(path, sheet_name=sheetname)

    charge_data = df[["Cycle", "CapD"]].to_numpy()

    plt.plot(
        charge_data[:, 0],
        charge_data[:, 1] / mass,
        linestyle="-",
        marker="o",
        color="b",
    )
    plt.xlabel("Cycle number")
    plt.ylabel("Specific Discharge capacity (mAh/g)")
    plt.title("Capacity over cycle life")
    plt.show()
