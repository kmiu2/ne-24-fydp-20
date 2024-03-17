import numpy as np
from analysis.helper import cut_off_cycle, cut_off_record
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
    is_anode,
    df_cycle,
    df_record,
    df_step,
    mass,
    voltage,
    helper_parameters,
):
    # Get Data
    cycle_data = df_cycle[["Cycle", "CapC", "CapD", "Efficiency"]].to_numpy()
    record_data = df_record[
        ["Cycle Count", "Current", "Voltage", "Step", "Step Mode"]
    ].to_numpy()
    step_data = df_step[["Step", "Mode", "Period", "Capacity"]].to_numpy()

    # Cut off pre-cycles
    # Also remove last cycle since its incomplete
    cycle_data = cut_off_cycle(cycle_data, helper_parameters)
    record_data = cut_off_record(record_data, helper_parameters)

    print("\n---------- Customer Requirements ----------")
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
    print(f"Avg Coulombic Efficiency: {(avg_coulombic_efficiency):.5f}%")
    print(f"Cycle Life: {cycle_life:.2f} cycles")

    ## Energy Efficiency, Charge Rate, Energy Density
    # - Integral [across 1 cycle] of (Current x Voltage x dt)
    # - Charge Rate = Energy / Time
    # - Energy Density = Energy / Mass

    # Get index of each new charge cycle
    cycle_indices = []
    for i in range(1, len(record_data)):
        # Skip rest steps
        if record_data[i][4] == "Rest" or record_data[i - 1][4] == "Rest":
            continue

        # If new step mode, add index
        if record_data[i][4] != record_data[i - 1][4]:
            cycle_indices.append(i)

    # Calculate energy and time for each CCC and CCD
    energies = []
    run_times = []
    for i in range(len(cycle_indices) - 1):
        # Get indices for each cycle
        start = cycle_indices[i]
        end = cycle_indices[i + 1]

        # Get current, voltage data, calculate time
        cycle_current = record_data[start:end, 1]  # mA
        cycle_current = cycle_current / 1000  # A
        cycle_voltage = record_data[start:end, 2]  # V
        time_interval = 10  # seconds
        time = time_interval * np.arange(cycle_current.size)
        time = time / 3600  # hours

        # Calculate energies
        energy = simpson(abs(cycle_current * cycle_voltage), time)  # Wh
        energies.append(energy)

        # Also calculate time
        run_time = time[-1]
        run_times.append(run_time)

    # Calculate energy efficiencies, charge rates, energy densities
    energy_efficiencies = []
    charge_rates = []
    discharge_energy_densities = []

    for i in range(0, len(energies) - 1, 2):
        # Energy Efficiency = (Energy in CCD) / (Energy in CCC)
        energy_ccd = energies[i + 1]
        energy_ccc = energies[i]
        energy_efficiency = min(energy_ccd, energy_ccc) / max(energy_ccd, energy_ccc)
        energy_efficiencies.append(energy_efficiency)

        # Charge Rate = Energy / Time
        charge_rate = energies[i] / run_times[i]
        charge_rates.append(charge_rate)

        # Energy Density = Energy / Mass
        discharge_energy_density = energy_ccd / mass
        discharge_energy_densities.append(discharge_energy_density)

    print(f"\nMax Charge Rate: {np.max(charge_rates):.4f} W")
    print(f"Avg Charge Rate: {np.mean(charge_rates):.4f} W")
    print(f"\nMax Energy Efficiency: {(np.max(energy_efficiencies)*100):.2f}%")
    print(f"Avg Energy Efficiency: {(np.mean(energy_efficiencies)*100):.2f}%")

    if is_anode:
        wh_cycle_data = np.array(cycle[1]) * voltage / 1000
        gravimetric_energy_density = wh_cycle_data / mass
        print(
            f"\nMax Gravimetric Energy Density: {np.max(gravimetric_energy_density):.2f} Wh/kg"
        )
        print(
            f"Avg Gravimetric Energy Density: {np.mean(gravimetric_energy_density):.2f} Wh/kg"
        )
    else:
        print(
            f"\nMax Gravimetric Energy Density: {np.mean(discharge_energy_densities):.2f} Wh/kg"
        )
        print(
            f"Avg Gravimetric Energy Density: {np.mean(discharge_energy_densities):.2f} Wh/kg"
        )
