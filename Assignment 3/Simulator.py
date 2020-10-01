# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 02:08:15 2020

@author: krish
"""

# =============================================================================
# Required modules
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Simulator definition
# =============================================================================

class Simulator:
    def __init__(self):
        self.hasFailed = False
        self.downTime = 0.0
        self.monthlyProduction = np.zeros(12)
        self.ProductionLossByUnit = np.zeros(3)

    def MonteCarloSimulation(self, facility, numberOfTrials, missionTime):
        stats = dict()
        failureCount = 0
        downTime = 0
        Production = 0
        monthlyProduction = np.zeros(12)
        ProductionLossByUnit = np.zeros(3)
        for trial in range(numberOfTrials):
            self.DrawExecution(facility, missionTime)
            if self.hasFailed:
                failureCount += 1
            downTime += self.downTime
            monthlyProduction += self.monthlyProduction/(missionTime/12)
            ProductionLossByUnit += self.ProductionLossByUnit/missionTime
        ProbabilityOfFailure = failureCount/numberOfTrials
        MeanDownTime = downTime/numberOfTrials
        MonthlyProduction = monthlyProduction/numberOfTrials
        Production = Production/numberOfTrials
        ProductionLossByUnit = ProductionLossByUnit/numberOfTrials
        self.PlotMonthlyProduction(MonthlyProduction)
        stats["Probability of failure"] = round(ProbabilityOfFailure,2)
        stats["Mean down time"] = round(MeanDownTime,2)
        stats["Production loss due to separator"] = round(ProductionLossByUnit[0],2)
        stats["Production loss due to dehydrators"] = round(ProductionLossByUnit[1],2)
        stats["Production loss due to compressor"] = round(ProductionLossByUnit[2],2)
        return stats
    
    def PlotMonthlyProduction(self, MonthlyProduction):
        X = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        Y = MonthlyProduction
        plt.plot(X, Y,)
        plt.savefig("Monthly Production")
        

    def SetStates(self, facility):
        for unit in facility.GetUnits():
            unit.working = True
            
    def DrawDurationsOfTransitions(self, units):
        duration = units.DrawDuration()
        return duration
    
    def SelectTransitionUnit(self, units, itemIndex):
        SelectedUnit = units[itemIndex]
        return SelectedUnit

    def AssessMonthlyProduction(self,missionTime, currentTime, previousCurrentTime, facilityCapacity):
        if currentTime <= (missionTime/12):
            self.monthlyProduction[0] += (currentTime - previousCurrentTime)*facilityCapacity
        elif currentTime > (missionTime/12) and currentTime <= ((2*missionTime)/12) :
            self.monthlyProduction[1] += (currentTime - previousCurrentTime)*facilityCapacity            
        elif currentTime > ((2*missionTime)/12) and currentTime <= ((3*missionTime)/12) :
            self.monthlyProduction[2] += (currentTime - previousCurrentTime)*facilityCapacity      
        elif currentTime > ((3*missionTime)/12) and currentTime <= ((4*missionTime)/12) :
           self.monthlyProduction[3] += (currentTime - previousCurrentTime)*facilityCapacity     
        elif currentTime > ((4*missionTime)/12) and currentTime <= ((5*missionTime)/12) :
            self.monthlyProduction[4] += (currentTime - previousCurrentTime)*facilityCapacity      
        elif currentTime > ((5*missionTime)/12) and currentTime <= ((6*missionTime)/12) :
            self.monthlyProduction[5] += (currentTime - previousCurrentTime)*facilityCapacity 
        elif currentTime > ((6*missionTime)/12) and currentTime <= ((7*missionTime)/12) :
            self.monthlyProduction[6] += (currentTime - previousCurrentTime)*facilityCapacity             
        elif currentTime > ((7*missionTime)/12) and currentTime <= ((8*missionTime)/12) :
            self.monthlyProduction[7] += (currentTime - previousCurrentTime)*facilityCapacity             
        elif currentTime > ((8*missionTime)/12) and currentTime <= ((9*missionTime)/12) :
            self.monthlyProduction[8] += (currentTime - previousCurrentTime)*facilityCapacity             
        elif currentTime > ((9*missionTime)/12) and currentTime <= ((10*missionTime)/12) :
            self.monthlyProduction[9] += (currentTime - previousCurrentTime)*facilityCapacity             
        elif currentTime > ((10*missionTime)/12) and currentTime <= ((11*missionTime)/12) :
            self.monthlyProduction[10] += (currentTime - previousCurrentTime)*facilityCapacity             
        else:
            self.monthlyProduction[11] += (currentTime - previousCurrentTime)*facilityCapacity             

    def AssessDownTime(self, currentTime, previousCurrentTime, facilityCapacity):
        if facilityCapacity == 0:
            self.hasFailed = True
            self.downTime += currentTime - previousCurrentTime                     

    def AssessProductionLossByUnit(self, currentTime, previousCurrentTime, facilityCapacity):
        if facilityCapacity == 55:
            self.ProductionLossByUnit[0] += 45*(currentTime-previousCurrentTime)
        elif facilityCapacity == 65:
            self.ProductionLossByUnit[1] += 35*(currentTime-previousCurrentTime)
        elif facilityCapacity == 52:
            self.ProductionLossByUnit[2] += 48*(currentTime-previousCurrentTime)
        elif facilityCapacity == 0 :
            self.ProductionLossByUnit[0] += 100*(currentTime-previousCurrentTime)
            self.ProductionLossByUnit[1] += 100*(currentTime-previousCurrentTime)
            self.ProductionLossByUnit[2] += 100*(currentTime-previousCurrentTime) 
    
    def RepairTimeUnlimitedRepairCrew(self,TransitionUnit, durations, itemIndex):
        durations[itemIndex] = TransitionUnit.DrawDuration()

    def RepairTimeOneRepairCrew(self,units, TransitionUnit, durations, itemIndex):
        waitingTime = []
        if TransitionUnit.working:
             durations[itemIndex] = TransitionUnit.DrawDuration()
        else:
            for unit in units:
                if unit.working == False:
                    unitIndex = units.index(unit)
                    waitingTime.append(durations[unitIndex])
            durations[itemIndex] = TransitionUnit.DrawDuration() + max(waitingTime)
            
    def DrawExecution(self, facility, missionTime):        
        self.SetStates(facility)        
        units = facility.GetUnits()        
        durations = np.zeros(len(units))
        for i in range(len(units)):
            durations[i] = self.DrawDurationsOfTransitions(units[i])
        currentTime = 0
        self.hasFailed = False
        self.downTime = 0.0
        self.production = 0.0
        self.ProductionLossByUnit = np.zeros(3)
        self.monthlyProduction = np.zeros(12)      
        while currentTime < missionTime:
            lowestDuration = min(durations) 
            itemIndex = np.where(durations == lowestDuration)[0][0]
            TransitionUnit = self.SelectTransitionUnit(units, itemIndex)
            facilityCapacity = facility.GetFacilityCapacity()            
            previousCurrentTime = currentTime           
            if currentTime + lowestDuration < missionTime:
                currentTime += lowestDuration    
            else:
                currentTime = missionTime
            self.AssessMonthlyProduction(missionTime, currentTime, previousCurrentTime, facilityCapacity)
            self.AssessDownTime(currentTime, previousCurrentTime, facilityCapacity) 
            self.AssessProductionLossByUnit(currentTime, previousCurrentTime, facilityCapacity)             
            TransitionUnit.Transition()
            durations = durations - lowestDuration
            self.RepairTimeUnlimitedRepairCrew(TransitionUnit, durations, itemIndex)
#            self.RepairTimeOneRepairCrew(units, TransitionUnit, durations, itemIndex)  ###alter here to assess performance with one repair crew
    
    
    
    
    