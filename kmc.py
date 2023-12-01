# Kinetic Monte Carlo simulation of adsorption and desorption of Sodium atoms on Al foil
import numpy as np
import matplotlib.pyplot as plt


def run_kmc(num_runs):
    ## Input parameters
    alpha = 1  # Strength of near neighbor interaction
    ra = 1e-7  # Adsorption rate, https://doi.org/10.3390/ma10070761
    rd = 0.2e-7  # Desorption rate
    length = 32  # Length of the foil (number of sites)

    ## Rates Setup
    rates = np.zeros(6)  # Rates of adsorption and desorption
    rates[0] = ra

    # Rates of desorption with respect to number of neighbours
    # rdi = rd * alpha**i where i is the number of neighbours (0 to 4)

    for i in range(1, 6):
        num_neighbours = i - 1
        rates[i] = rd * alpha**num_neighbours

    ## Simulation Setup
    lattice = np.zeros(
        (length + 2, length + 2)
    )  # Lattice of atoms (with extra sites for periodic boundary conditions)
    prob = np.zeros(6)  # Probability of each rate event
    results = np.zeros(num_runs)  # Results of the simulation

    ## Main Loop
    for run in range(num_runs):
        # Matrix to store locations
        sites = [[] for _ in range(6)]
        num_times = np.zeros(6)  # Number of times each rate event occurs

        for i in range(1, length + 1):
            for j in range(1, length + 1):
                if lattice[i, j] == 0:
                    num_times[0] += 1
                    sites[0].append((i, j))
                elif lattice[i, j] == 1:
                    num_neighbours = int(
                        lattice[i - 1, j]
                        + lattice[i + 1, j]
                        + lattice[i, j - 1]
                        + lattice[i, j + 1]
                    )
                    num_times[num_neighbours] += 1
                    sites[num_neighbours].append((i, j))

        # Calculate total rate
        total_rate = 0
        for i in range(6):
            total_rate += num_times[i] * rates[i]

        # Calculate probabilities
        prob[0] = num_times[0] * rates[0] / total_rate
        for i in range(5):
            prob[i + 1] = prob[i] + num_times[i + 1] * rates[i + 1] / total_rate

        # Choose event
        rand = np.random.random()

        # Adsorption event
        if rand <= prob[0]:
            temp = np.floor(np.random.random() * num_times[0] + 1)
            if temp > num_times[0]:
                temp = num_times[0]
            temp = int(temp) - 1

            x = sites[0][temp][0]
            y = sites[0][temp][1]
            lattice[x, y] = 1

            # Periodic boundary conditions
            if x == 1:
                lattice[length + 1, y] = 1
            elif x == length:
                lattice[0, y] = 1

            if y == 1:
                lattice[x, length + 1] = 1
            elif y == length:
                lattice[x, 0] = 1

        # Desorption event
        elif rand > prob[0]:
            for i in range(5):
                if prob[i] < rand <= prob[i + 1]:
                    temp = np.floor(np.random.random() * num_times[i + 1] + 1)
                    if temp > num_times[i + 1]:
                        temp = num_times[i + 1]
                    temp = int(temp) - 1

                    x = sites[i + 1][temp][0]
                    y = sites[i + 1][temp][1]
                    lattice[x, y] = 0

                    # Periodic boundary conditions
                    if x == 1:
                        lattice[length + 1, y] = 0
                    elif x == length:
                        lattice[0, y] = 0

                    if y == 1:
                        lattice[x, length + 1] = 0
                    elif y == length:
                        lattice[x, 0] = 0

        ## Record results
        # Calculate fractional coverage
        coverage = np.sum(lattice[1 : length + 1, 1 : length + 1]) / length**2
        results[run] = coverage

    return results


## Run multiple times
num_runs = 10
num_steps = 5000  # Number of MC steps
results = np.zeros((num_runs, num_steps))
for i in range(num_runs):
    print(f"Run {i + 1} of {num_runs}")
    results[i] = run_kmc(num_steps)


# Get an array of the average coverage at each step
avg_results = np.zeros(num_steps)
std_results = np.zeros(num_steps)
for i in range(num_steps):
    avg_results[i] = np.mean(results[:, i])
    std_results[i] = np.std(results[:, i])

## Plotting
steps = np.arange(1, num_steps + 1)
plt.figure()
plt.plot(steps, avg_results, color="orange", label="Average coverage")
plt.fill_between(
    steps,
    avg_results - std_results,
    avg_results + std_results,
    alpha=0.2,
    label="Standard deviation",
)
plt.xlabel("Steps")
plt.ylabel("Coverage")
plt.title("Coverage vs Steps")
plt.legend()
plt.show()
