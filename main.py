import pybamm
from sympy import solve

pybamm.set_logging_level("NOTICE")

# List of Chemistries
# https://docs.pybamm.org/en/latest/source/api/parameters/parameter_sets.html#parameter-sets
# ['Ai2020', 'Chen2020', 'Chen2020_composite', 'ECM_Example', 'Ecker2015', 'Marquis2019', 'Mohtat2020',
# 'NCA_Kim2011', 'OKane2022', 'ORegan2022', 'Prada2013', 'Ramadass2004', 'Sulzer2019', 'Xu2019']


def quick_simulation():
    print("Running quick simulation")
    model = pybamm.lithium_ion.DFN()
    sim = pybamm.Simulation(model)
    sim.solve([0, 60])
    sim.plot()


# From: https://docs.pybamm.org/en/latest/source/examples/notebooks/getting_started/tutorial-5-run-experiments.html
# See also: https://youtu.be/2SrfbpVnXwI
def cycle_test():
    print("Running cycle test")

    # Parameter values
    num_of_cycles = 100
    parameter_values = pybamm.ParameterValues("Mohtat2020")
    parameter_values.update({"SEI kinetic rate constant [m.s-1]": 1e-14})

    # Set up experiment
    experiment = pybamm.Experiment(
        [
            (
                "Charge at 1C until 4.2V",
                "Hold at 4.2V until C/50",
                "Discharge at 1C until 3V",
                "Rest for 1 hour",
            ),
        ]
        * num_of_cycles,
        termination="80% capacity",
    )

    # Model and simulation
    model = pybamm.lithium_ion.SPM({"SEI": "ec reaction limited"})

    sim = pybamm.Simulation(
        model, experiment=experiment, parameter_values=parameter_values
    )
    sim.solve()
    sol = sim.solution

    # Plot
    sol.plot(
        [
            "Negative electrode stoichiometry",
            "Positive electrode stoichiometry",
            "Total lithium in particles [mol]",
            "Loss of lithium due to loss of active material in negative electrode [mol]",
            "X-averaged inner SEI thickness [m]",
        ]
    )


# Run the simulations
cycle_test()
