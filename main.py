from parameters import mohtat2020
from scipy.integrate import simps
import numpy as np
import pybamm

pybamm.set_logging_level("NOTICE")


def find_indices_in_range(entries, lower, upper):
    arr = np.where(np.logical_and(entries > lower, entries < upper))[0]
    start = arr[0]
    end = start

    # Discharge end is when the indexes stop increasing by strictly 1
    prev_val = arr[0] - 1
    for i, value in enumerate(arr):
        if value != prev_val + 1:
            end = arr[i - 1]
            break
        prev_val = value

    return start, end


def cycle_test():
    print("*** Running cycle test ***")

    ## Simulation
    # Parameter values
    # num_of_cycles = 2000
    num_of_cycles = 5
    cut_off_percent = 85
    parameter_values = pybamm.ParameterValues("Mohtat2020")
    parameter_values.update(mohtat2020)

    # Set up experiment
    experiment = pybamm.Experiment(
        [
            (
                "Discharge at C/6 until 3.5V",
                "Rest for 1 hour",
                "Charge at 2C until 3.8V",
                "Hold at 3.8V until C/50",
            ),
        ]
        * num_of_cycles,
        termination=f"{cut_off_percent}% capacity",
    )

    # Model and simulation
    model_options = {"SEI": "ec reaction limited"}
    model = pybamm.lithium_ion.SPM(model_options)
    sim = pybamm.Simulation(
        model,
        experiment=experiment,
        parameter_values=parameter_values,
    )
    sim.solve()

    # Plot
    sim.plot(
        [
            "Current [A]",
            "Voltage [V]",
        ]
    )

    ## Calculations
    print("-----------------------------------")
    sol = sim.solution

    # Energy Density
    # Integrate over time
    # Cut time off so it's only discharge.
    # Take where current is first 5/6 until it stops being 5/6.
    discharge_start, discharge_end = find_indices_in_range(
        sol["Current [A]"].entries, 0.82, 0.84
    )

    time = sol["Time [h]"].entries[discharge_start:discharge_end]
    voltage = sol["Voltage [V]"].entries[discharge_start:discharge_end]
    current = sol["Current [A]"].entries[discharge_start:discharge_end]

    watt_hours = simps(voltage * current, time)
    print(f"Watt hours: {watt_hours:.3f} Wh")

    cell_volume = parameter_values["Cell volume [m3]"]
    cell_volume_cm3 = cell_volume * 1e6
    vol_energy_density = watt_hours / cell_volume_cm3
    print(f"Volumetric energy density: {vol_energy_density:.3f} Wh/cm3")

    electrode_area = (
        parameter_values["Electrode height [m]"]
        * parameter_values["Electrode width [m]"]
    )
    negative_electrode_weight = (
        parameter_values["Negative electrode thickness [m]"]
        * 0.1
        * electrode_area
        * parameter_values["Negative electrode density [kg.m-3]"]
    )
    positive_electrode_weight = (
        parameter_values["Positive electrode thickness [m]"]
        * electrode_area
        * parameter_values["Positive electrode density [kg.m-3]"]
    )
    separator_weight = (
        parameter_values["Separator thickness [m]"]
        * electrode_area
        * parameter_values["Separator density [kg.m-3]"]
    )
    cell_weight = (
        negative_electrode_weight + positive_electrode_weight + separator_weight
    )
    grav_energy_density = watt_hours / cell_weight
    print(f"Gravimetric energy density: {grav_energy_density:.3f} Wh/kg")

    print("-----------------------------------")
    # Charging Rate
    # Cut time off so it's only charge (around -10A).
    charge_start, charge_end = find_indices_in_range(
        sol["Current [A]"].entries, -10.1, -9.9
    )
    time = sol["Time [h]"].entries[charge_start:charge_end]
    voltage = sol["Voltage [V]"].entries[charge_start:charge_end]
    current = sol["Current [A]"].entries[charge_start:charge_end]
    power = voltage * current
    avg_power = np.mean(power)
    print(f"Average power: {avg_power:.3f} W")
    print("-----------------------------------")


# Run the simulations
cycle_test()
