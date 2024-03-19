# Quick script to print out the actual rates for the current rates
base_rate = 2.23
start = 0.1
end = 1.00
increment = 0.05
c_rates = []
for i in range(int((end - start) / increment) + 1):
    c_rates.append(round((start + i * increment), 2))

actual_rates = [round(base_rate * i, 2) for i in c_rates]

for i in range(len(c_rates)):
    print(f"{c_rates[i]:.2f} C \t {actual_rates[i]:.2f} A")
