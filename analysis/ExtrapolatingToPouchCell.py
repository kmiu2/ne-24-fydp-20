# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:12:46 2024

@author: David
"""
# input parameters based on the test battery
#  Cathode and Anode Performance
cathodeEnergyDensity = 1.19 # Wh/kg
anodeEnergyDensity = 400 # Wh/kg
#  Cathode and Anode Film and Substrate properties
anodeMass = 9.9 # mg - weight of the whole electrode (active material + susbstrate)
cathodeMass = 30 # mg - weight of the whole electrode (active material + susbstrate)
anodeSubstrateMass = 8.5 # mg - estimated weight of either the Cu or Al foil the anode is deposited on
cathodeSubstrateMass = 8.5 # mg - estimated weight of either the Cu or Al foil the cathode is deposited on
cathodeActiveMaterial = 0.5 # _ - decimal for the volume % of active material used in the cathode
#  Coating Recipe Details
#   Anode
CBinAnode = 0.75 # g/g_totalSolid
NaCMCsInAnode = 0.25 # g/g_totalSolid
TritonXinAnode = 0.35 # v% in solution
CBwtInWater = 0.3/14 # decimal of wt% CB in liquid (assume ethanol = 1g/ml)
EthanolVolumeToWater = 4/14 # ratio of volume ethanol / total volume used for dispersion
#   Cathode
rGOinCathode = 0.05 # weight fraction to total solids
NaCMCsInCathode = 0.475 # weight fraction of NaCMCs to total solids
PBAinCathode = 0.475 # weight fraction to total solids
TritonXinCathode = 0.01 # v% in solution
CathodeSolnVolume = 15 # mL volume total of liquids
#   Alternative Cathode Performance Parameters for full cell performance
useAlt = True # sets if the alternative enrgy density should be used
CathActEnergyDensityAlt  = 250 # Wh/kg, alternative active material energy density to be used
CathActR = 0.97 # weight fraction active material
condcFillerR = 0.02 # weight fraction conductive filler




# input parameters based on outside sources
# costs
carbonBlackCost = 24 # $/kg
PBA_precursorsCost = 0.0 # $/kg
AlFoilCost = 0.0 #note units for this when I source it
CuFoilCost = 0.0 #note units for this when I source it
NaCMCsCost = 0.0 # $/kg
TritonXCost = 0.0 #
EthanolCost = 0.0 #
WaterCost = 0.0 # not sure if I should inlude this?
rGOCost = 0.0 #
pouchCellMaterialCost = 0.38 #USD/m2
seperatorCost = 3.04 # USD/m^2 : 31USD per roll / (6cm[roll Width]*170m[roll Length])
CADfromUSD = 1.35 # multiplier to get from USD to CAD
# Densities
carbonBlackDensity = 0.160 # 
PBADensity = 1.83 # 
AlFoilDensity = 2.710 # g/cm^3
CuFoilDensity = 0.0 #note units for this when I source it
NaCMCsDensity = 1.6 # 
rGODensity = 0.3 #
pouchCellMaterialDensity = 45 # g/m^2
seperatorDensity = 0.92 # g/cm3
electrolyteDensity = 0.937 # g/ml
# PouchCellDimensions
pouch_L = 12.5 # cm
pouch_H = 0.2 # cm
pouch_W = 5.0 # cm
layers = 1
pouch_Area = pouch_L * pouch_W
pouch_SurfaceArea = 2*pouch_Area + 2*(pouch_H*pouch_L + pouch_H*pouch_W)
# Pouch Cell Materials Dimensions
CurrentCollectorThick = 0.012 # mm
SeparatorThick = 0.025 # mm
ElectrolytePerUnitArea = 0.225 # mL/cm^2 : this is ~3x what we use in a coin cell to be generous



#Performing Calculations
# extrapolating cathode performance
CathActEnergyDensity = cathodeEnergyDensity * cathodeMass / ((cathodeMass - cathodeSubstrateMass) * cathodeActiveMaterial)
Cath90ActDensity = CathActEnergyDensity * 0.9
Cath97ActDensity = CathActEnergyDensity * 0.97
# finding the anode energy density of active material
AnodeActEnergyDensity = anodeEnergyDensity * anodeMass / (anodeMass - anodeSubstrateMass)

# Determine average densities of anode and cathode
AnodeDensity = carbonBlackDensity*0.8 + NaCMCsDensity*0.2
CathodeDensity = PBADensity*CathActR + rGODensity*condcFillerR + (1-CathActR-condcFillerR)*NaCMCsDensity


# determining ideal volume ratios
if useAlt:
    VolRatioCtoA = anodeEnergyDensity / CathActEnergyDensityAlt
else:
    VolRatioCtoA = anodeEnergyDensity / CathActEnergyDensity
# find layer thicknesses
FullLayerThick = pouch_H / layers
CathThick = (FullLayerThick - SeparatorThick - CurrentCollectorThick)*(VolRatioCtoA/(VolRatioCtoA+1))
AnodeThick = FullLayerThick - SeparatorThick - CurrentCollectorThick -CathThick
# find component masses
PouchCellMatMass = pouch_SurfaceArea * pouchCellMaterialDensity /10000
CathMass = CathodeDensity*pouch_Area*CathThick * layers
AnodeMass = AnodeDensity*pouch_Area*AnodeThick * layers
SeperatorMass = seperatorDensity*pouch_Area*SeparatorThick * layers
CurrentCollectorMass = AlFoilDensity*pouch_Area*CurrentCollectorThick * (layers+1)
volumeElectrolyte = ElectrolytePerUnitArea * pouch_Area
MassElectrolyte = ElectrolytePerUnitArea * electrolyteDensity
TotalMass = PouchCellMatMass + CathMass + AnodeMass + SeperatorMass + CurrentCollectorMass + MassElectrolyte

# calculate overall energy Densities
BatGravEnergyDensity = AnodeMass*AnodeActEnergyDensity/TotalMass


print(AnodeMass*AnodeActEnergyDensity/TotalMass)
print(AnodeMass/1000*AnodeActEnergyDensity/(pouch_L*pouch_H*pouch_W))

print(FullLayerThick)
print(CathThick+SeparatorThick+CurrentCollectorThick+AnodeThick)
print((CathThick+SeparatorThick+CurrentCollectorThick+AnodeThick)*layers)
print(VolRatioCtoA)
print(CathThick)
print(AnodeThick)



print(f"Cathode Active Material Gravimetric Energy Denisty: {CathActEnergyDensity}")
print(f"Cathode With 90% Active Material Gravimetric Energy Denisty: {Cath90ActDensity}")
print(f"Cathode With 97% Active Material Gravimetric Energy Denisty: {Cath97ActDensity}")




