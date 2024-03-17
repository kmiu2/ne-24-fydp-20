# Plot discharge capacity as a function of cycle number - check units!
# Need to figure out how to get specific capacity as well
import matplotlib.pyplot as plt
import numpy as np
from analysis.helper import cut_off_cycle, cut_off_record
from scipy.integrate import simpson


def discharge_capacity(
    is_anode,
    df_cycle,
    df_record,
    mass,
    voltage,
    helper_parameters,
    save_plots,
):
    # Get data from each column
    cycle_data = df_cycle[["Cycle", "CapC", "CapD"]].to_numpy()
    record_data = df_record[
        ["Cycle Count", "Current", "Voltage", "Step", "Step Mode"]
    ].to_numpy()

    # Cut off pre-cycles
    cycle_data = cut_off_cycle(cycle_data, helper_parameters)
    record_data = cut_off_record(record_data, helper_parameters)

    if is_anode:
        wh_cycle_data = np.array(cycle_data[:, 1]) * voltage / 1000
        x = cycle_data[:, 0]
        y = wh_cycle_data / mass
    else:
        cycle_indices = []
        for i in range(1, len(record_data)):
            if record_data[i][4] == "Rest" or record_data[i - 1][4] == "Rest":
                continue
            if record_data[i][4] != record_data[i - 1][4]:
                cycle_indices.append(i)

        energies = []
        for i in range(len(cycle_indices) - 1):
            start = cycle_indices[i]
            end = cycle_indices[i + 1]
            cycle_current = record_data[start:end, 1]  # mA
            cycle_current = cycle_current / 1000  # A
            cycle_voltage = record_data[start:end, 2]  # V
            time_interval = 10  # seconds
            time = time_interval * np.arange(cycle_current.size)
            time = time / 3600  # hours
            energy = simpson(abs(cycle_current * cycle_voltage), time)  # Wh
            energies.append(energy)

        discharge_energy_densities = []
        for i in range(0, len(energies) - 1, 2):
            energy_ccd = energies[i + 1]
            discharge_energy_density = energy_ccd / mass
            discharge_energy_densities.append(discharge_energy_density)

        x = cycle_data[:, 0]
        y = discharge_energy_densities

    # Cut off the last extra x element if len(x) > len(y)
    if len(x) > len(y):
        x = x[: len(y)]

    # Plotting
    plt.clf()
    plt.plot(
        x,
        y,
        linestyle="-",
        marker="o",
        color="#38761d",
    )
    plt.xlabel("Cycle Number")
    plt.ylabel("Specific Discharge Capacity (Wh/kg)")
    plt.title("Capacity vs. Cycles")
    plt.grid()
    if save_plots:
        plt.savefig("graphs/discharge_capacity.png", dpi=300, bbox_inches="tight")
    else:
        plt.show()
