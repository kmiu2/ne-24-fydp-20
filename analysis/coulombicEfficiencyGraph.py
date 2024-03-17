import matplotlib.pyplot as plt
from analysis.helper import cut_off_cycle


def columbic_efficiency(df_cycle, helper_parameters, save_plots):
    # Get data from each column
    cycle_data = df_cycle[["Cycle", "CapC", "CapD", "Efficiency"]].to_numpy()

    # Cut off pre-cycles
    cycle_data = cut_off_cycle(cycle_data, helper_parameters)

    # Coulombic Efficiency
    # - Loop through all entries
    # - Take the larger of CapC and CapD as the denominator
    # - Average to get the efficiency
    adjusted_efficiencies = []
    for cycle in cycle_data:
        capC = cycle[1]
        capD = cycle[2]
        adjusted_efficiency = min(capC, capD) / max(capC, capD) * 100
        adjusted_efficiencies.append(adjusted_efficiency)

    # Plotting
    plt.clf()
    plt.plot(
        cycle_data[:, 0],
        adjusted_efficiencies,
        linestyle="-",
        marker="o",
        color="#38761d",
    )
    plt.xlabel("Cycle Number")
    plt.ylabel("Columbic Efficiency (%)")
    plt.title("Efficiency vs. Cycles")
    plt.grid()
    if save_plots:
        plt.savefig("graphs/columbic_efficiency.png", dpi=300, bbox_inches="tight")
    else:
        plt.show()
