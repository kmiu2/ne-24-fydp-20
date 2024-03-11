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
    cycle_data = df_cycle[["Cycle", "CapD", "Efficiency"]].to_numpy()

    # Cut off pre-cycles
    cycle_data = cut_off_cycle(cycle_data, remove_one=True)

    print("\n---------- Customer Requirements ----------")

    # Gravimetric Energy Density
    wh_cycle_data = cycle_data[:, 1] * voltage / 1000
    gravimetric_energy_density = wh_cycle_data / mass
    print(
        f"Max Gravimetric Energy Density: {np.max(gravimetric_energy_density):.2f} Wh/kg"
    )
    print(
        f"Avg Gravimetric Energy Density: {np.mean(gravimetric_energy_density):.2f} Wh/kg"
    )

    # Cycle Life
    avg_coulombic_efficiency = np.mean(cycle_data[:, 2])
    cycle_life = np.log(0.8) / np.log(avg_coulombic_efficiency / 100)
    print(f"Avg Coulombic Efficiency: {(avg_coulombic_efficiency):.6f}%")
    print(f"Cycle Life: {cycle_life:.2f} cycles")
