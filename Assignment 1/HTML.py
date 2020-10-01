# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 14:09:11 2020

@author: krish
"""
import Core
import re
import sys
import TSVparser
import SequenceChecker
import Calculator
#import EnergyConsumptionPlots

#-----------------------------------------------------------------------------------
# Serializer 
#-----------------------------------------------------------------------------------

class HTMLSerializer:
    def __init__(self):
        self.indentation = "\t"
        self.depth = 0
    
    
    def SerializeListOfCircuitElements(self, circuit):
        result = self.SerializeOpenTag("ul")
        self.depth += 1
        for element in circuit.GetAllElements():
            result += self.SerializeOpenTag("li")
            self.depth += 1
            result += self.SerializeElementDescription(element)
            self.depth -= 1
            result += self.SerializeCloseTag("li")
        self.depth -= 1
        result += self.SerializeCloseTag("ul")
        return result
    

    def SerializeElementDescription(self, element):
        if element.GetType() == 'tank':
            return f'{element.GetType()}: {element.GetName()}'
        elif element.GetType() == 'pipe':
            length = self.SerializeAttributeValue(element.GetLength())
            diameter = self.SerializeAttributeValue(element.GetDiameter())
            angle = self.SerializeAttributeValue(element.GetAngle())
            return f'{element.GetType()}: {element.GetName()} - Length: {length}, Diameter: {diameter}, Angle: {angle}'
        elif element.GetType() == 'bend':
            diameter = self.SerializeAttributeValue(element.GetDiameter())
            return f'{element.GetType()}: {element.GetName()} - Diameter: {diameter}'
        elif element.GetType() == 'pump':
            efficiency = self.SerializeAttributeValue(element.GetEfficiency())
            return f'{element.GetType()}: {element.GetName()} - Efficiency: {efficiency}'
        elif element.GetType() == 'valve':
            state = self.SerializeAttributeValue(element.GetStatus())
            return f'{element.GetType()}: {element.GetName()} - State: {state}'
        elif element.GetType() == 'filter':
            state = self.SerializeAttributeValue(element.GetStatus())
            return f'{element.GetType()}: {element.GetName()} - State: {state}'
    
    def SerializeEnergyConsumption(self, circuit):
        calculator = Calculator.Calculator(circuit)
        energyConsumption = calculator.CalculateActualEnergyConsumption(circuit)
        result = self.SerializeOpenTag("ul")
        self.depth += 1
        result += f'Energy Consumption = {(energyConsumption)} kW'
        self.depth -= 1
        result += self.SerializeCloseTag("ul")
        return result
    
    def SerializeEfficiencyPlot(self, circuit, plotName1):
        consumptionPlot = Calculator.Calculator(circuit)
        consumptionPlot.EnergyConsumptionAndPumpEfficiency(circuit)
        return "<img src='" + plotName1 + "' alt='hey' width='460' height='345'>"
    
    def SerializeDiameterPlot(self, circuit, plotName2):
        consumptionPlot = Calculator.Calculator(circuit)
        consumptionPlot.EnergyConsumptionAndDiameter(circuit)
        return "<img src='" + plotName2 + "' alt='hey' width='460' height='345'>"
    
    def SerializeHeightPlot(self, circuit, plotName3):
        consumptionPlot = Calculator.Calculator(circuit)
        consumptionPlot.EnergyConsumptionAndHeight(circuit)
        return "<img src='" + plotName3 + "' alt='hey' width='460' height='345'>"
    
    def SerializeValvePlot(self, circuit, plotName4):
        consumptionPlot = Calculator.Calculator(circuit)
        consumptionPlot.EnergyConsumptoionAndValves(circuit)
        return "<img src='" + plotName4 + "' alt='hey' width='460' height='345'>"
    
    def SerializeFilterPlot(self, circuit, plotName5):
        consumptionPlot = Calculator.Calculator(circuit)
        consumptionPlot.EnergyConsumptoionAndFilter(circuit)
        return "<img src='" + plotName5 + "' alt='hey' width='460' height='345'>"

        
    def SerializeSequenceChecker(self, circuit):
        result = self.SerializeOpenTag("ul")
        self.depth += 1
        result += 'The given circuit satisfies all the conditions above'
        self.depth -= 1
        result += self.SerializeCloseTag("ul")
        return result
    
    def SerializeAttributeValue(self, value):
        return "{0:.2f}".format(value)
        
    def SerializeIndentation(self):
        result = ""
        for de in range(0, self.depth):
          result += self.indentation
        return result
    
    def SerializeOpenTag(self, name):
        return self.SerializeIndentation() + "<" + name + ">\n"
    
    def SerializeCloseTag(self, name):
        return self.SerializeIndentation() + "</" + name + ">\n"


#-----------------------------------------------------------------------------------------------------------
# HTML Creator      
#-----------------------------------------------------------------------------------------------------------

class HTMLCreator:
    def __init__(self):
        self.serializer = HTMLSerializer()
        
    def ExportCircuitAtHTMLFormat(self, circuit, templateFileName, targetFileName, plotName1, plotName2, plotName3, plotName4, plotName5):
        try:
            templateFile = open(templateFileName, 'r')
        except:
            sys.stderr.write('Unable to open file "%s"\n' % templateFileName)
            sys.stderr.flush()
            return 1
        try:
            targetFile = open(targetFileName, 'w')
        except:
            sys.stderr.write('Unable to open file "%s"\n' % targetFileName)
            sys.stderr.flush()
            templateFile.close()
            return 1
        self.PrintReport(circuit,templateFile, targetFile, plotName1, plotName2, plotName3, plotName4, plotName5)
        templateFile.close()
        targetFile.flush()
        targetFile.close()
        return 0
    
    def PrintReport(self, circuit, templateFile, targetFile, plotName1, plotName2, plotName3, plotName4, plotName5):
        for line in templateFile:
            line = line.rstrip()
            if re.search(r'__CIRCUIT__', line):
                line = re.sub(r'__CIRCUIT__', self.serializer.SerializeListOfCircuitElements(circuit), line)
            elif re.search(r'__SequenceChecker__', line):
                line = re.sub(r'__SequenceChecker__', self.serializer.SerializeSequenceChecker(circuit), line)
            elif re.search(r'__ENERGYCONSUMPTION__', line):
                line = re.sub(r'__ENERGYCONSUMPTION__', self.serializer.SerializeEnergyConsumption(circuit), line)
            elif re.search(r'__EFFICIENCYPLOT__', line):
                line = re.sub(r'__EFFICIENCYPLOT__', self.serializer.SerializeEfficiencyPlot(circuit, plotName1), line)
            elif re.search(r'__DIAMETERPLOT__', line):
                line = re.sub(r'__DIAMETERPLOT__', self.serializer.SerializeDiameterPlot(circuit, plotName2), line)
            elif re.search(r'__HEIGHTPLOT__', line):
                line = re.sub(r'__HEIGHTPLOT__', self.serializer.SerializeHeightPlot(circuit, plotName3), line)
            elif re.search(r'__VALVEPLOT__', line):
                line = re.sub(r'__VALVEPLOT__', self.serializer.SerializeValvePlot(circuit, plotName4), line)
            elif re.search(r'__FILTERPLOT__', line):
                line = re.sub(r'__FILTERPLOT__', self.serializer.SerializeFilterPlot(circuit, plotName5), line)
            targetFile.write(line + '\n')
            
            
        
      


