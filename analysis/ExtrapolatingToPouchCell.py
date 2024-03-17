# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:12:46 2024

@author: David
"""
# input parameters based on the test battery
#  Cathode and Anode Performance
cathodeEnergyDensity = 100 # Wh/kg
anodeEnergyDensity = 195 # Wh/kg
#  Cathode and Anode Film and Substrate properties
anodeMass = 10.7 # mg - weight of the whole electrode (active material + susbstrate)
cathodeMass = 21.8 # mg - weight of the whole electrode (active material + susbstrate)
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
CathActEnergyDensityAlt  = 180 # Wh/kg, alternative active material energy density to be used
CathActR = 0.97 # weight fraction active material
condcFillerR = 0.02 # weight fraction conductive filler




# input parameters based on outside sources
# costs
carbonBlackCost = 24 # $/kg
PBA_precursorsCost = (9.35*4 + 5.275*2)/5.5 # CuSO4 + pottatium ferrocyanide over product yield $/kg
AlFoilCost = 2.10 #USD / kg
CuFoilCost = 0.0 #note units for this when I source it /// dont need this
NaCMCsCost = 0.3 # $/kg
CNF_Cost = 1.4560 # USD/g
TritonXCost = 1.0 * 1.06 # $/L = $/kg * kg/L
EthanolCost = 1.21 * 0.789 # USD/L
WaterCost = 0.0 # not sure if I should inlude this?
rGOCost = 122.5 # USD/g
pouchCellMaterialCost = 0.38 #USD/m2
seperatorCost = 3.04 # USD/m^2 : 31USD per roll / (6cm[roll Width]*170m[roll Length])
CADfromUSD = 1.35 # multiplier to get from USD to CAD
ElectrolyteCost = 3.2*0.937 + 0.10979*0.1*2 + 0.1695*0.9*2 # USD/L diglyme + USD/1L of 0.1M NaBF4 + USD/1L of 0.9M NaPF6
# Densities
carbonBlackDensity = 0.160 # 
PBADensity = 1.83 # g/cm^3
AlFoilDensity = 2.710 # g/cm^3
CuFoilDensity = 0.0 #note units for this when I source it
NaCMCsDensity = 1.6 # g/cm3
rGODensity = 0.3 #g/cm3
pouchCellMaterialDensity = 45 # g/m^2
seperatorDensity = 0.92 # g/cm3
electrolyteDensity = 0.937 # g/ml
# PouchCellDimensions
pouch_L = 12.5 # cm
pouch_H = 0.2 # cm
pouch_W = 5.0 # cm
layers = 1
# Pouch Cell Materials Dimensions
CurrentCollectorThick = 0.0006 # cm
SeparatorThick = 0.0025 # cm
ElectrolytePerUnitArea = 0.075 # mL/cm^2 : this is ~3x what we use in a coin cell to be generous



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

def pouchCalcs (AED, AD, CED, CD, CathRecipe, l = pouch_L, w = pouch_W, h = pouch_H, AnodeRecipe = [0.8, 0.2, 0.03, 0.4]):
    '''
    Parameters
    ----------
    AED : TYPE
        Anode Energy Density.
    AD : TYPE
        Anode Density.
    CED : TYPE
        Cathode Energy Density.
    CD : TYPE
        Cathode Density.
    l : TYPE
        pouch cell length.
    w : TYPE
        pouch cell width.
    h : TYPE
        pouch cell height.
    CathRecipe : List of floats
        [Activematerial%, NaCMC%, CNF%, rGO%, CB%].
    AnodeRecipe : List of floats
        [CB%, Binder%, %CBtoLiquid, EthanolToWater].
    
    Returns
    -------
    BatGravED : TYPE
        DESCRIPTION.
    BatVolED : TYPE
        DESCRIPTION.

    '''
    #find ratio of anode to cathode volume wise
    R = (AED*AD) / (CED*CD)  
    #find thickness of a layer
    Lt = h / layers
    #find thickness of anode and cathode in those layers
    Ct = (Lt - SeparatorThick - CurrentCollectorThick)*(R/(R+1))
    At = Lt - SeparatorThick - CurrentCollectorThick - Ct
    #find face and surface area of pouch cell and volume
    PCA = l * w 
    PCSA = 2*(h*l + h*w + PCA)
    V = l * w * h
    #find componennt masses
    PCM = PCSA * pouchCellMaterialDensity / 10000
    CM = CD*PCA*Ct*layers
    AM = AD*PCA*At*layers
    SepM = seperatorDensity*PCA*SeparatorThick*layers
    CCM = AlFoilDensity*PCA*CurrentCollectorThick*(layers+1)
    volE = ElectrolytePerUnitArea*PCA
    EM = volE*electrolyteDensity
    TM = PCM + CM + AM + SepM + CCM + EM
    #find energy stored
    Energy = CM*CED/1000
    print(CED)
    print(AED)
    print(Energy)
    #find overall energy density
    BatGravED = Energy/TM*1000
    BatVolED = Energy/V
    #find costs in USD
    PBAC = CM*CathRecipe[0]*PBA_precursorsCost/1000
    NaCMCsC = (CM*CathRecipe[1] + AM*AnodeRecipe[1])*NaCMCsCost/1000
    CNFC = CM*CathRecipe[2]*CNF_Cost
    rGOC = CM*CathRecipe[3]*rGOCost
    CBC = (CM*CathRecipe[4] + AM*AnodeRecipe[0])*carbonBlackCost/1000
    EthanolC = AM*AnodeRecipe[0]*(1/(1+AnodeRecipe[2]))*AnodeRecipe[3]/1000
    TritonXC = AM*AnodeRecipe[0]*(1/(1+AnodeRecipe[2]))*0.0035/1000
    SepC = PCA * layers * seperatorCost/10000
    PCC = PCSA * pouchCellMaterialCost/10000
    CCC = CCM*AlFoilCost/1000
    ElectrolyteC = volE * ElectrolyteCost/1000
    TotalCost = PBAC + NaCMCsC + CNFC + rGOC + CBC + EthanolC + TritonXC + SepC + PCC + CCC + ElectrolyteC
    #Conver Cost to CAD
    TotalCostCAD = TotalCost*CADfromUSD
    #Find cost per kWh
    CostPerKWh = TotalCostCAD/Energy*1000
    
    print(TotalCost)
    
    return (BatGravED, BatVolED, CostPerKWh)


OurBat = pouchCalcs(AnodeActEnergyDensity, AnodeDensity, CathActEnergyDensity*.45, 
                    CathodeDensity, [0.45, 0.45, 0.00, 0, 0.1])
CNFBat = pouchCalcs(AnodeActEnergyDensity, AnodeDensity, CathActEnergyDensity*.87, 
                    CathodeDensity, [0.87, 0.02, 0.01, 0, 0.1])


print(OurBat)
print(CNFBat)

print(f"Cathode Active Material Gravimetric Energy Denisty: {CathActEnergyDensity}")
print(f"Cathode With 90% Active Material Gravimetric Energy Denisty: {Cath90ActDensity}")
print(f"Cathode With 97% Active Material Gravimetric Energy Denisty: {Cath97ActDensity}")




