# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 02:27:02 2020

@author: krish
"""
# =============================================================================
# Imported modules
# =============================================================================

import DataStructure
import MonteCarloSimulation
import XMLInterface
import Classifier
import Regressor
import HTMLInterface


# =============================================================================
# Main body
# =============================================================================

diagram = DataStructure.Diagram()
xmlParser = XMLInterface.XMLParser()
xmlParser.ImportDiagramXMLFormat('ControlSystemProject.xml', diagram)
calculator = MonteCarloSimulation.Calculator()
checker = MonteCarloSimulation.Checker()
classifier = Classifier.Classifier()
regressor = Regressor.Regressor()
htmlInterface = HTMLInterface.HTMLCreator()
if checker.CheckConstraints(diagram) is True:
    noOfTrials= 10000
    statistics = calculator.MeasureStatistics(noOfTrials, diagram)
    histogramName = "Histogram"
    gateName = "MidProject"
    accuracyOfClassificationMethods = classifier.AccuracyOfClassificationMethods(noOfTrials, diagram, gateName)
    accuracyOfRegressionMethods = regressor.AccuracyOfRegressionMethods(noOfTrials, diagram, gateName)
    templateFile = "DiagramTemplate.html"
    targetFile = "Risk Assessment.html"
    htmlInterface.ExportDiagramAtHTMLFormat(diagram, templateFile, targetFile, statistics, histogramName, accuracyOfClassificationMethods, accuracyOfRegressionMethods)