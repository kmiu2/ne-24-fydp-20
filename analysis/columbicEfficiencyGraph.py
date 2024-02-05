import matplotlib.pyplot as plt
from helper import cut_off_cycle


def columbic_efficiency(df):
    # Get data from each column
    charge_data = df[["Cycle", "Efficiency"]].to_numpy()

    # Cut off pre-cycles
    charge_data = cut_off_cycle(charge_data)

    # Plotting
    plt.plot(
        charge_data[:, 0],
        charge_data[:, 1],
        linestyle="-",
        marker="o",
        color="b",
    )
    plt.xlabel("Cycle Number")
    plt.ylabel("Columbic Efficiency (%)")
    plt.title("Efficiency Over Cycle Life")
    plt.show()
