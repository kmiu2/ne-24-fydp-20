import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def voltage_time(path, sheetname):
    df = pd.read_excel(path, sheet_name=sheetname)

    charge_data = df[["Voltage"]].to_numpy()
    x = 10 * np.arange(charge_data.size)

    plt.plot(x, charge_data, color="darkviolet")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage over cycle life")
    plt.show()
