# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 01:56:14 2020

@author: krish
"""

# =============================================================================
# Required modules
# =============================================================================

import sys
import DataStructure
import XMLInterface
import numpy as np
import matplotlib.pyplot as plt
import random

# =============================================================================
# Checker
# =============================================================================

class Checker:
    def __init__(self):
        pass
  
    def CheckConstraints(self, diagram):
        self.Condition1(diagram)
        self.Condition2(diagram)
        return True
 
    def Condition1(self, diagram):
        count = 0
        nodes = diagram.GetNodes()
        for node in nodes:
            if len(node.predecessors) == 0:
                count += 1
                if count >1 or node.type != 0:
                    sys.exit("Condition 1 not met")
            else:
                return True

    def Condition2(self, diagram):
        count = 0
        nodes = diagram.GetNodes()
        for node in nodes:
            if len(node.successors) == 0:
                count += 1
                if count >1 or node.type != 0:
                    sys.exit("Condition 2 not met")
            else:
                return True  
            
# =============================================================================
# Calculations for Monte-Carlo simulation
# =============================================================================

class Calculator:
    def __init__(self):
        pass
    
    def CalculateDurationOfEachTask(self, diagram):
        lanes = diagram.lanes
        for lane in lanes:
            workLoad = random.random()
            for task in lanes[lane]:
                minDuration = lanes[lane][task].minDuration
                maxDuration = lanes[lane][task].maxDuration
                expectedDuration = minDuration + (maxDuration - minDuration) * workLoad
                lanes[lane][task].duration = np.random.triangular(minDuration, expectedDuration, maxDuration)
                
                
    def CalculateTotalDuration(self, diagram):
        nodes = diagram.GetNodes()
        self.CalculateDurationOfEachTask(diagram)
        self.ResetDates(diagram)
        while self.CheckIfStartAndEndDateIsCalculated(nodes) == 1:
            for node in nodes:
                if len(node.predecessors) == 0:
                    node.startDate = 0
                    node.completionDate = node.startDate + node.duration
                else:
                    if self.CheckIfStartAndEndDateIsCalculated(node.predecessors) == 0:
                        node.startDate = self.CompletionDateOfPredecessors(node)
                        node.completionDate = node.startDate + node.duration
        endOfProject = None
        for node in nodes:
            if len(node.successors) == 0:
                endOfProject = node
        return endOfProject.completionDate

    def ResetDates(self, diagram):
        for node in diagram.GetNodes():
            node.startDate = -1
            node.completionDate = -1
        return 0
    
    def CheckIfStartAndEndDateIsCalculated(self, nodes):
        for node in nodes:
            if node.startDate == -1 or node.completionDate == -1:
                return 1
        return 0
        
    def CompletionDateOfPredecessors(self, node):
        completionDates = []
        for task in node.predecessors:
            completionDates.append(task.completionDate)
        LongestCompletionDate = max(completionDates)
        return LongestCompletionDate
    
    def MonteCarloSimulation(self, noOfTrials, diagram):
        totalDuration = np.zeros(noOfTrials)
        for index in range(noOfTrials):
            totalDuration[index] = self.CalculateTotalDuration(diagram)
        return totalDuration
    
    def MeasureStatistics(self, noOfTrials, diagram):
        stats = dict()
        SimulatedDurations = self.MonteCarloSimulation(noOfTrials, diagram )
        stats["Average duration"] = round(SimulatedDurations.mean(),2)
        stats["Minimum duration"] = round(SimulatedDurations.min(),2)
        stats["Maximum duration"] = round(SimulatedDurations.max(),2)
        stats["0.5 quantile"] = round(np.quantile(SimulatedDurations, 0.5),2)
        stats["0.9 quantile"] = round(np.quantile(SimulatedDurations, 0.9),2)
        plt.hist(SimulatedDurations, 100, density=True)
        plt.title(" Histogram for the simulation")
        plt.xlabel("Total duration of the project")
        plt.ylabel(" Number of occurances")
        plt.savefig("Histogram")
        plt.close()
        return stats
        
    def CompletionDatesOfNodesBeforeGivenGate(self, diagram, gateName):
        ascendants = []
        diagram.nodes[gateName].CollectAscendants(ascendants)
        completionDate = np.zeros(10)
        for index in range(len(ascendants)):
            completionDate[index] = ascendants[index].completionDate
        return completionDate
            
        



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    