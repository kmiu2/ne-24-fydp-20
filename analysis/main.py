from chargeDischargeGraph import capacity_graph
from dischargeCapacityCyclingGraph import dischargeCapacity
from columbicEfficiencyGraph import columbicEfficiency
from voltageTimeGraph import voltageTime

path = "003_8.xlsx"

capacity_graph(path, sheetname="Record", mass=0.0006)
dischargeCapacity(path, sheetname="Cycle", mass=0.0006)
columbicEfficiency(path, sheetname="Cycle")
voltageTime(path, sheetname="Record")
