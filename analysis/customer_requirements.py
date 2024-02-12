import numpy as np
from helper import cut_off_cycle

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
    cycle_data = df_cycle[["Cycle", "CapD"]].to_numpy()

    # Cut off pre-cycles
    cycle_data = cut_off_cycle(cycle_data)

    print("\n---------- Customer Requirements ----------")

    # Gravimentric Energy Density
    wh_cycle_data = cycle_data[:, 1] * voltage / 1000
    gravimetric_energy_density = wh_cycle_data / mass
    print(
        f"Max Gravimetric Energy Density: {np.max(gravimetric_energy_density):.2f} Wh/kg"
    )
    print(
        f"Avg Gravimetric Energy Density: {np.mean(gravimetric_energy_density):.2f} Wh/kg"
    )
