import pandas as pd
import matplotlib.pyplot as plt


def columbicEfficiency(path, sheetname):
    df = pd.read_excel(path, sheet_name=sheetname)

    charge_data = df[["Cycle", "Efficiency"]].to_numpy()

    plt.plot(
        charge_data[:, 0],
        charge_data[:, 1],
        linestyle="-",
        marker="o",
        color="b",
    )
    plt.xlabel("Cycle number")
    plt.ylabel("Coulombic Efficiency (%)")
    plt.title("Efficiency over cycle life")
    plt.show()
