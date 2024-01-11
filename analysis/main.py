from chargeDischargeGraph import capacity_graph
from dischargeCapacityCyclingGraph import discharge_capacity
from columbicEfficiencyGraph import columbic_efficiency
from voltageTimeGraph import voltage_time

path = "003_8.xlsx"

capacity_graph(path, sheetname="Record", mass=0.0006)
discharge_capacity(path, sheetname="Cycle", mass=0.0006)
columbic_efficiency(path, sheetname="Cycle")
voltage_time(path, sheetname="Record")
