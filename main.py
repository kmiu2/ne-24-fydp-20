from matplotlib import pyplot as plt
from scipy.integrate import simps
import numpy as np
import pybamm
from parameters import mohtat2020

pybamm.set_logging_level("NOTICE")


def cycle_test():
    print("*** Running cycle test ***")

    ## Simulation
    # Parameter values
    # num_of_cycles = 2000
    num_of_cycles = 1
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

    # solver = pybamm.CasadiSolver(mode="fast with events", atol=1e-6, rtol=1e-6)
    # model = pybamm.lithium_ion.DFN(model_options)

    sim = pybamm.Simulation(
        model,
        experiment=experiment,
        parameter_values=parameter_values,
        # solver=solver,
    )
    sim.solve()

    # Plot
    sim.plot(
        [
            "Current [A]",
            "Voltage [V]",
            "Total lithium capacity [A.h]",
            "Loss of lithium to SEI [mol]",
        ]
    )

    ## Calculations
    sol = sim.solution

    # Energy Density
    # Integrate over time
    time = sol["Time [h]"].entries

    # Cut time off so it's only discharge.
    # Take everything from first index till it hits 3.5V
    index_to_stop = np.where(sol["Voltage [V]"].entries < 3.501)[0][0]
    time = time[:index_to_stop]
    voltage = sol["Voltage [V]"].entries[:index_to_stop]
    current = sol["Current [A]"].entries[:index_to_stop]

    watt_hours = simps(voltage * current, time)
    print(watt_hours)

    cell_volume = parameter_values["Cell volume [m3]"]
    cell_volume_cm3 = cell_volume * 1e6
    vol_energy_density = watt_hours / cell_volume_cm3
    print(f"Volumetric energy density: {vol_energy_density} Wh/cm3")


# Run the simulations
cycle_test()
