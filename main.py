import pybamm

print("Starting simulation...")
model = pybamm.lithium_ion.DFN()  # Doyle-Fuller-Newman model
sim = pybamm.Simulation(model)
sim.solve([0, 60])
sim.plot()
