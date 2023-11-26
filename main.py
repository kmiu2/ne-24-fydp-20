from matplotlib import pyplot as plt
import numpy as np
import pybamm
from parameters import mohtat2020

pybamm.set_logging_level("NOTICE")


def cycle_test():
    print("*** Running cycle test ***")

    # Parameter values
    num_of_cycles = 1000
    cut_off_percent = 80
    parameter_values = pybamm.ParameterValues("Mohtat2020")
    parameter_values.update(mohtat2020)

    # Set up experiment
    experiment = pybamm.Experiment(
        [
            (
                "Discharge at 1C until 1.75V",
                "Rest for 1 hour",
                "Charge at 1C until 2.8V",
                "Hold at 2.8V until C/50",
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

    # Capacity calculation
    print("----------------------")
    initial_capacity = sol["Total lithium capacity [A.h]"].entries[0]
    final_capacity = sol["Total lithium capacity [A.h]"].entries[-1]
    percent_capacity_loss = (initial_capacity - final_capacity) / initial_capacity * 100
    print(f"Capacity loss: {percent_capacity_loss}%")

    # Extrapolate to 80% capacity (capacity loss is currently 0.33%)
    cycles_to_80_percent = 20 / (percent_capacity_loss / 100) * num_of_cycles
    print("Cycles to 80% capacity:", cycles_to_80_percent)


# Run the simulations
cycle_test()
