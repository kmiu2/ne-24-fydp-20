# NE 24 FYDP Group 20

# Data Analysis

Run the main.py file in the root directory to analyze data.

# Simulations

## Create Environment and Install PyBaMM

See full [guide](https://docs.pybamm.org/en/latest/source/user_guide/installation/) at the official PyBaMM website.

```bash
conda create --name fydp python=3.8
conda activate fydp
conda install -c conda-forge pybamm
conda install -c conda-forge numpy
conda install -c conda-forge pandas
conda install -c conda-forge matplotlib
conda install -c conda-forge openpyxl
```

## Activate Environment

```bash
conda activate fydp
```

## Version

Uses PyBaMM version 23.5

## Links

- Link to the [PyBaMM Documentation](https://docs.pybamm.org/en/stable/index.html).
- Link to [video tutorials](https://pybamm.org/learn/).

## Troubleshooting

If you are getting pybamm not found/installed try activating the environment in VSCode. `CTRL + Shift + P` and then search for `Python: Select Interpreter` and choose the `fydp` environment. (Taken from this [post](https://stackoverflow.com/a/67750888/10014923))
