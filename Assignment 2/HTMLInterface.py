# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 02:59:52 2020

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
import re
import sys

# =============================================================================
# HTML serializer
# =============================================================================

class HTMLSerializer:
    def __init__(self):
        self.indentation = "\t"
        self.depth = 0
    
    def SerializeModelTableHeader(self):
        result = self.SerializeOpenTag("tr")
        self.depth += 1
        result += self.SerializeOpenTag("th")
        result += ' Lanes and Corresponding tasks'
        result += self.SerializeCloseTag("th")
        self.depth -= 1
        result += self.SerializeCloseTag("tr")
        return result
        
    def SerializeModelElements(self, diagram):
        result = self.SerializeOpenTag('table id="Table"')
        self.depth += 1
        result += self.SerializeModelTableHeader()
        for lane in diagram.lanes:
            result += self.SerializeOpenTag("tr")
            self.depth += 1
            result += self.SerializeOpenTag("td")
            result += self.SerializeOpenTag("b")
            result += lane
            result += self.SerializeCloseTag("b")
            result += self.SerializeCloseTag("td")
            result += self.SerializeCloseTag("tr")
            for task in diagram.lanes[lane]:    
                result += self.SerializeTasks(diagram, lane, task)
            self.depth -= 1
        self.depth -= 1
        result += self.SerializeCloseTag("table")
        return result
    
    def SerializeTasks(self, diagram, lane, task):
        result = self.SerializeOpenTag("tr")
        self.depth += 1
        result += self.SerializeOpenTag("td")
        result += task
        result += self.SerializeCloseTag("td")
        self.depth -= 1
        result += self.SerializeCloseTag("tr")
        return result
    
    def SerializeModelChecker(self, diagram):
        result = self.SerializeOpenTag("ul")
        self.depth += 1
        result += 'CONGRATULATIONS! THE MODEL SATISFIES ALL THE CONDITIONS.'
        self.depth -= 1
        result += self.SerializeCloseTag("ul")
        return result
    
    def SerializeMCSStatistics(self, statistics, histogramName):
        result = self.SerializeOpenTag('table id="Table"')
        self.depth += 1
        result += self.SerializeStatisticsHeader()
        for element in statistics:
            result += self.SerializeOpenTag('tr')
            self.depth += 1
            result += self.SerializeOpenTag("td")
            result += str(element)
            result += self.SerializeCloseTag("td")
            result += self.SerializeOpenTag("td")
            result += f'{statistics[element]}'
            result += self.SerializeCloseTag("td")
        self.depth -= 1
        result += self.SerializeCloseTag("table")
        return result
    
    def SerializeStatisticsHeader(self):
        result = self.SerializeOpenTag("tr")
        self.depth += 1
        result += self.SerializeOpenTag("th")
        result += 'Assessed Statistic'
        result += self.SerializeCloseTag("th")
        result += self.SerializeOpenTag("th")
        result += 'Simulated Value'
        result += self.SerializeCloseTag("th")
        self.depth -= 1
        result += self.SerializeCloseTag("tr")
        return result

    def SerializeClassificationHeader(self):
        result = self.SerializeOpenTag("tr")
        self.depth += 1
        result += self.SerializeOpenTag("th")
        result += 'Classification Model'
        result += self.SerializeCloseTag("th")
        result += self.SerializeOpenTag("th")
        result += '96'
        result += self.SerializeCloseTag("th")
        result += self.SerializeOpenTag("th")
        result += '102'
        result += self.SerializeCloseTag("th")
        result += self.SerializeOpenTag("th")
        result += '108'
        result += self.SerializeCloseTag("th")
        self.depth -= 1
        result += self.SerializeCloseTag("tr")
        return result    

    def SerializeClassificationAccuracy(self, accuracyOfClassificationMethods):
        result = self.SerializeOpenTag('table id="Table"')
        self.depth += 1
        result += self.SerializeClassificationHeader()
        for model in accuracyOfClassificationMethods:
            result += self.SerializeOpenTag("tr")
            self.depth += 1
            result += self.SerializeOpenTag("td")
            result += str(model)
            result += self.SerializeCloseTag("td")
            result += self.SerializeOpenTag("td")
            result += f'{round(accuracyOfClassificationMethods[model][0],2)}'
            result += self.SerializeCloseTag("td")
            result += self.SerializeOpenTag("td")
            result += f'{round(accuracyOfClassificationMethods[model][1],2)}'
            result += self.SerializeCloseTag("td")
            result += self.SerializeOpenTag("td")
            result += f'{round(accuracyOfClassificationMethods[model][2],2)}'
            result += self.SerializeCloseTag("td")
            self.depth -= 1
            result += self.SerializeCloseTag("tr")
        self.depth -= 1
        result += self.SerializeCloseTag("table")
        return result
    
    def SerializeRegressionAccuracy(self, accuracyOfRegressionMethods):
        result = self.SerializeOpenTag('table id="Table"')
        self.depth += 1
        result += self.SerializeRegressionHeader()
        for model in accuracyOfRegressionMethods:
            result += self.SerializeOpenTag("tr")
            self.depth += 1
            result += self.SerializeOpenTag("td")
            result += str(model)
            result += self.SerializeCloseTag("td")
            result += self.SerializeOpenTag("td")
            result += f'{round(accuracyOfRegressionMethods[model], 2)}'
            result += self.SerializeCloseTag("td")
        self.depth -= 1
        result += self.SerializeCloseTag("table")
        return result
        
        
    def SerializeRegressionHeader(self):
        result = self.SerializeOpenTag("tr")
        self.depth += 1
        result += self.SerializeOpenTag("th")
        result += 'Regression Model'
        result += self.SerializeCloseTag("th")
        result += self.SerializeOpenTag("th")
        result += 'Accuracy'
        result += self.SerializeCloseTag("th")
        self.depth -= 1
        result += self.SerializeCloseTag("tr")
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
    
# =============================================================================
# HTML maker    
# =============================================================================

class HTMLCreator:
    def __init__(self):
        self.serializer = HTMLSerializer()
        
    def ExportDiagramAtHTMLFormat(self, diagram, templateFile, targetFile, statistics, histogramName, accuracyOfClassificationMethods, accuracyOfRegressionMethods):
        try:
            templateFile = open(templateFile, 'r')
        except:
            sys.stderr.write('Unable to open file "%s"\n' % templateFile)
            sys.stderr.flush()
            return 1
        try:
            targetFile = open(targetFile, 'w')
        except:
            sys.stderr.write('Unable to open file "%s"\n' % targetFile)
            sys.stderr.flush()
            templateFile.close()
            return 1
        self.PrintReport(diagram, templateFile, targetFile, statistics, histogramName, accuracyOfClassificationMethods, accuracyOfRegressionMethods)
        templateFile.close()
        targetFile.flush()
        targetFile.close()
        return 0
    
    def PrintReport(self, diagram, templateFile, targetFile, statistics, histogramName, accuracyOfClassificationMethods, accuracyOfRegressionMethods):
        for line in templateFile:
            line = line.rstrip()
            if re.search(r'__MODEL__', line):
                line = re.sub(r'__MODEL__', self.serializer.SerializeModelElements(diagram), line)
            elif re.search(r'__CHECKER__', line):
                line = re.sub(r'__CHECKER__', self.serializer.SerializeModelChecker(diagram), line)
            elif re.search(r'__STATISTICS__', line):
                line = re.sub(r'__STATISTICS__', self.serializer.SerializeMCSStatistics(statistics, histogramName), line)
            elif re.search(r'__CLASSIFICATION__', line):
                line = re.sub(r'__CLASSIFICATION__', self.serializer.SerializeClassificationAccuracy(accuracyOfClassificationMethods), line)
            elif re.search(r'__REGRESSION__', line):
                line = re.sub(r'__REGRESSION__', self.serializer.SerializeRegressionAccuracy(accuracyOfRegressionMethods), line)
            targetFile.write(line + '\n')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    