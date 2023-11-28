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
    voltage = sol["Terminal voltage [V]"].entries
    current = sol["Current [A]"].entries

    wh = simps(voltage * current, time)
    print(wh)


# Run the simulations
cycle_test()
