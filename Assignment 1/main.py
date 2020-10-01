# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 20:36:28 2020

@author: krish
"""
from Core import *
from SequenceChecker import *
from Calculator import *
from XMLparser import *
from TSVparser import *
from HTML import *

circuit = Circuit()
tsvparser = TSVParser()
xmlParser = XMLParser()
htmlInterface = HTMLCreator()

#xmlParser.ImportCircuitXMLFormat(circuit, 'circuit.xml')
tsvparser.ImportFile(circuit, "test.tsv") 
sequence = SequenceChecker.SequenceChecker(circuit)
Checker = sequence.Checker(circuit)
#calculator = Calculator.Calculator(circuit)
#calculator.PerformCalculations(circuit)
#calculator.EnergyConsumptionAndPumpEfficiency(circuit)
#calculator.EnergyConsumptionAndDiameter(circuit)
#calculator.EnergyConsumptionAndHeight(circuit)
#calculator.EnergyConsumptoionAndValves(circuit)
#calculator.EnergyConsumptoionAndFilter(circuit)
if Checker is True:   
    templateFileName = "CircuitTemplate.html"
    targetFileName = "Circuit.html"
    plotName1 = "Energy Consumption Vs PumpEfficiency.png"
    plotName2 = "Energy Consumption Vs Diameter.png"
    plotName3 = "Energy Consumption Vs Height.png"
    plotName4 = "Energy Consumption Vs Valve.png"
    plotName5 = "Energy Consumption Vs Filter.png"
    htmlInterface.ExportCircuitAtHTMLFormat(circuit, templateFileName, targetFileName, plotName1, plotName2, plotName3, plotName4, plotName5)