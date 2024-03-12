import numpy as np
from analysis.helper import cut_off_cycle

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

    # Cut off pre-cycles
    # Also remove last cycle since its incomplete
    cycle_data = cut_off_cycle(cycle_data, remove_one=True)

    print("\n---------- Customer Requirements ----------")

    # Gravimetric Energy Density
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

    # Cycle Life
    # - Loop through all entries
    # - Take the larger of CapC and CapD as the denominator
    # - Average to get the efficiency
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
