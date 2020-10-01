# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 01:52:30 2020

@author: krish
"""

# =============================================================================
# imported modules
# =============================================================================
import Core
import Simulator
import HTMLinterface

# =============================================================================
# Body
# =============================================================================

facility = Core.MarkovSystem()
simulator = Simulator.Simulator()
htmlInterface = HTMLinterface.HTMLCreator()

facility.AddUnit("HPS_A", "Separators", 8.91e-5, 2.54e-3, 55)
facility.AddUnit("HPS_B", "Separators", 8.91e-5, 2.54e-3, 55)
facility.AddUnit("HPS_C", "Separators", 8.91e-5, 2.54e-3, 55)

facility.AddUnit("DEH_A","Dehydrators", 3.11e-5, 3.95e-3, 65)
facility.AddUnit("DEH_B","Dehydrators", 3.11e-5, 3.95e-3, 65)

facility.AddUnit("CMP_A","Compressors",5.5e-5, 5.14e-3, 52)
facility.AddUnit("CMP_B","Compressors",5.5e-5, 5.14e-3, 52)

numberOfTrials = 10000
missionTime = 100000
statistics = simulator.MonteCarloSimulation(facility, numberOfTrials, missionTime)
templateFile = "FacilityTemplate.html"
targetFile = "Prodction Assessment of the facility.html"
htmlInterface.ExportHTMLFormat(templateFile, targetFile, statistics)
