import numpy as np
from analysis.helper import cut_off_cycle
from scipy.integrate import simpson

## Customer Requirements
# Primary:
# - Gravimetric Energy Density: > 200 Wh/kg
# - Cost: < $150/kWh
# - Cycle Life: > 700 cycles
# - Energy Efficiency: > 85%
# Secondary:
# - Enhanced Cycle Life: > 1000 cycles
# - Volume Energy Density: > 0.5 Wh/cm3
# - Charge Rate: > 15 W
# - Sustainability: 0% rare earth metals


def print_customer_requirements(
    df_cycle,
    df_record,
    df_step,
    mass,
    voltage,
):
    # Get Data
    cycle_data = df_cycle[["Cycle", "CapC", "CapD", "Efficiency"]].to_numpy()
    record_data = df_record[
        ["Cycle Count", "Current", "Voltage", "Step", "Step Mode"]
    ].to_numpy()

    # Cut off pre-cycles
    # Also remove last cycle since its incomplete
    cycle_data = cut_off_cycle(cycle_data)
    record_data = cut_off_cycle(record_data)

    print("\n---------- Customer Requirements ----------")

    ## Gravimetric Energy Density
    # - Wh = mAh * V / 1000
    # - Wh/kg = Wh / kg
    wh_cycle_data = cycle_data[:, 1] * voltage / 1000
    gravimetric_energy_density = wh_cycle_data / mass
    print(
        f"Max Gravimetric Energy Density: {np.max(gravimetric_energy_density):.2f} Wh/kg"
    )
    print(
        f"Avg Gravimetric Energy Density: {np.mean(gravimetric_energy_density):.2f} Wh/kg"
    )

    ## Cycle Life
    # - Loop through all entries
    # - Take the larger of CapC and CapD as the denominator
    # - Average to get the coulombic efficiency
    adjusted_efficiencies = []
    for cycle in cycle_data:
        capC = cycle[1]
        capD = cycle[2]
        adjusted_efficiency = min(capC, capD) / max(capC, capD)
        adjusted_efficiencies.append(adjusted_efficiency)
    avg_coulombic_efficiency = np.mean(adjusted_efficiencies) * 100

    # - Since: Remaining Capacity = Efficiency ^ Cycles
    # - Cycle Life = log(Remaining Capacity) / log(avg_coulombic_efficiency)
    cycle_life = np.log(0.8) / np.log(avg_coulombic_efficiency / 100)
    print(f"\nAvg Coulombic Efficiency: {(avg_coulombic_efficiency):.5f}%")
    print(f"Cycle Life: {cycle_life:.2f} cycles")

    ## Energy Efficiency
    # - Integral [across 1 cycle] of (Current x Voltage x dt)

    # Get index of each new charge cycle
    cycle_indices = []
    for i in range(1, len(record_data)):
        # Skip rest steps
        if record_data[i][4] == "Rest" or record_data[i - 1][4] == "Rest":
            continue

        # If new step mode, add index
        if record_data[i][4] != record_data[i - 1][4]:
            cycle_indices.append(i)

    # Calculate energy for each CCC and CCD
    energies = []
    for i in range(len(cycle_indices) - 1):
        # Get indices for each cycle
        start = cycle_indices[i]
        end = cycle_indices[i + 1]

        # Get current, voltage data, calculate time
        current = record_data[start:end, 1]
        voltage = record_data[start:end, 2]
        time_interval = 10  # seconds
        time = time_interval * np.arange(current.size)

        # Calculate energies
        energy = simpson(current * voltage, time)
        energies.append(abs(energy))

    # Calculate energy efficiencies
    energy_efficiencies = []
    for i in range(0, len(energies) - 1, 2):
        energy_efficiency = energies[i + 1] / energies[i]
        energy_efficiencies.append(energy_efficiency)

    avg_energy_efficiency = np.mean(energy_efficiencies) * 100
    print(f"\nAvg Energy Efficiency: {avg_energy_efficiency:.2f}%")
