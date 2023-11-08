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
                "Charge at 1C until 4.2V",
                "Hold at 4.2V until C/50",
                "Discharge at 1C until 3V",
                "Rest for 1 hour",
            ),
        ]
        * num_of_cycles,
        termination=f"{cut_off_percent}% capacity",
    )

    # Model and simulation
    model_options = {"SEI": "ec reaction limited"}
    model = pybamm.lithium_ion.SPM(model_options)
    sim = pybamm.Simulation(
        model, experiment=experiment, parameter_values=parameter_values
    )
    sim.solve()

    # Plot
    sim.plot(
        [
            "Current [A]",
            "Total current density [A.m-2]",
            "Voltage [V]",
            "Discharge capacity [A.h]",
            "Electrolyte potential [V]",
            "Electrolyte concentration [mol.m-3]",
            "Total SEI thickness [m]",
            "Negative electrode porosity",
            "X-averaged negative electrode porosity",
            "X-averaged negative electrode SEI interfacial current density [A.m-2]",
            "X-averaged total SEI thickness [m]",
            [
                "Total lithium lost [mol]",
                "Loss of lithium to SEI [mol]",
            ],
        ]
    )


# Run the simulations
cycle_test()
