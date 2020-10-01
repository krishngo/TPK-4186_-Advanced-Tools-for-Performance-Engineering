# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 23:31:34 2020

@author: krish
"""

import sys
from Core import *
import math
import numpy as np
import matplotlib.pyplot as plt

class Calculator():
    def __init__(self,circuit):
        self.testCircuit = circuit.GetAllElements()
        self.density = 1025
        self.gravity = 9.81
        self.diameter = self.testCircuit[1].diameter #pump is the second element
        self.kinematicVelocity = 1.35e-6
        self.height = self.TotalHeight(circuit)
        self.valveState = self.GetValveStatus(circuit)
        self.filterState = self.GetFilterStatus(circuit)
        self.velocityInterval = self.MaximumVelocity(self.diameter)
        
        
    def PerformCalculations(self,circuit):
        self.CalculateActualEnergyConsumption(circuit)
        
    def CalculateActualEnergyConsumption(self,circuit):
        efficiency = self.PumpEfficiency(circuit)
        diameter = self.diameter
#        ValveStatus = self.GetValveStatus(circuit)
#        FilterStatus = self.GetFilterStatus(circuit)
        TheoreticalEnergy = self.CalculateTheoreticalEnergy(circuit, self.velocityInterval[0], diameter, self.height, self.valveState, self.filterState  )
        ActualEnergy = TheoreticalEnergy/efficiency
        return round(ActualEnergy,3)
        
    def PumpEfficiency(self,circuit):
        for element in self.testCircuit:
            if element.type == "pump":
                efficiency = element.efficiency
        return efficiency

    def TotalHeight(self, circuit):
        TotalHeight = 0
        for element in self.testCircuit:
            if element.type == "pipe":
                if element.angle == 90:
                    height = element.length
                    TotalHeight += height
        return TotalHeight
    
    def GetValveStatus(self,circuit):
        ValveStatus = []
        for element in self.testCircuit:
            if element.type == "valve":
                Status = element.status
                ValveStatus.append(Status)
        return ValveStatus
    
    def GetFilterStatus(self,circuit):
        FilterStatus = []
        for element in self.testCircuit:
            if element.type == "filter":
                Status = element.status
                FilterStatus.append(Status)
        return FilterStatus    
    
    def CalculateTheoreticalEnergy(self, circuit, velocity, diameter, height, valveState, filterState):
        TotalFrictionalLoss = self.PipeLoss(circuit, velocity, diameter) + self.BendLoss(circuit, velocity) + self.ValveLoss(circuit, velocity, valveState) + self.FilterLoss(circuit, velocity, filterState)
        TheoreticalEnergy = ((self.PressureLossDueToHeight(circuit, height) + TotalFrictionalLoss) * self.FlowRate(velocity, diameter))/1000
        return TheoreticalEnergy
             
    def PressureLossDueToHeight(self, circuit, height):
        LossInPressureDueToHeight = self.height * self.density * self.gravity
        return LossInPressureDueToHeight
    
    def FlowRate(self, velocity, diameter):
        Area = (math.pi * diameter**2)/4
        FlowRate = Area*velocity
        return FlowRate
    
    def PipeLoss(self, circuit, velocity, diameter ):
        TotalLengthOfPipe = 0
        for element in self.testCircuit:
            if element.type == "pipe":
                TotalLengthOfPipe += element.length
        Re = (velocity * diameter)/(self.kinematicVelocity) #Re = Reynold's Number
        if Re < 2300:
            lamda = 64/Re
        elif Re >= 2300 and Re <= 1e5:
            lamda = 0.316/(math.pow(Re,1/4))
        else:
            sys.exit("Coefficient of flow in a point that is beyond the scope")
            lamda = 0.316/(math.pow(Re,1/4))
        LossOfPressureDueToPipe = ((lamda * self.density * velocity) / (diameter * 2 ))* TotalLengthOfPipe
        return LossOfPressureDueToPipe
    
    def BendLoss(self, circuit, velocity): 
        NumberOfBends= 0
        for element in self.testCircuit:
            if element.type == "bend":
                NumberOfBends += 1
        BendFactor = math.sin(math.pi/2) * 0.1 # only 90 degree considered
        LossOfPressureDueToBends = ((BendFactor * self.density * (velocity**2))  / 2) * NumberOfBends
        return LossOfPressureDueToBends
    
    def ValveLoss(self, circuit, velocity, valveState):
        self.valveState = valveState
        LossOfPressureDueToAllValve = 0
        for item in range (0,len(self.valveState)):
            if self.valveState[item] == 1:
                Coefficient = 0.2
            elif self.valveState[item] == 0.5:
                Coefficient = 4.0
            elif self.valveState[item] > 0.5 and self.valveState[item] < 1.0:
                Coefficient = self.LinearInterpolation(0.2, 4.0, 1.0, valveState, 0.5)
            else:
                print('Value for valve state out of bounds')
            LossOfPressure = Coefficient * (self.density / 2) * velocity**2
            LossOfPressureDueToAllValve += LossOfPressure
        return LossOfPressureDueToAllValve

    
    def LinearInterpolation(self, y0, y1, x0, x, x1):
        return (y0*(x1 - x) + y1*(x - x0)) / (x1 - x0)
    
    def FilterLoss (self, circuit, velocity, filterState):
        self.filterState = filterState
        LossOfPressureDueToAllFilter = 0
        for item in range (0,len(self.filterState)):
            if self.filterState[item] == 1:
                Coefficient = 0.5
            elif self.filterState[item] == 0.5:
                Coefficient = 5
            elif self.filterState[item] > 0.5 and self.filterState[item] < 1.0:
                Coefficient = self.LinearInterpolation(0.5, 5, 1.0, filterState, 0.5)
            else:
                print('Value for valve state out of bounds')
            LossOfPressure = Coefficient * (self.density / 2) * velocity**2
            LossOfPressureDueToAllFilter += LossOfPressure
        return LossOfPressureDueToAllFilter

    
    def MaximumVelocity(self, diameter):
        velocityMax = (1E5 * self.kinematicVelocity) / diameter
        velocityInterval = np.linspace(0.1, velocityMax, 5 )
        return velocityInterval
    

#-----------------------------------------------------------------------------------------------    
#Plot calculations
#-----------------------------------------------------------------------------------------------    
        
    def EnergyConsumptionAndPumpEfficiency(self,circuit):
        TEnergy = []
        ActualEnergy = []
        self.efficiency = np.linspace(0.7, 0.9, 20)
        self.velocityInterval = self.MaximumVelocity(self.diameter)
        self.valveState = self.GetValveStatus(circuit)
        self.filterState = self.GetFilterStatus(circuit)
        for i in range (0,5,1):
            velocity = self.velocityInterval[i]
            TE = self.CalculateTheoreticalEnergy(circuit, velocity, self.diameter, self.height, self.valveState, self.filterState)
            TEnergy.append(TE)

        for i in range(0, len(TEnergy)):
            TheoreticalEnergy = TEnergy[i]
            EnergyConsumed = TheoreticalEnergy/self.efficiency
            ActualEnergy.append(EnergyConsumed)

        
        Xs = np.linspace(0.7,0.9,20)
        
        Y1 = ActualEnergy[0]
        Y2 = ActualEnergy[1]
        Y3 = ActualEnergy[2]
        Y4 = ActualEnergy[3]
        Y5 = ActualEnergy[4]
        
        plt.plot(Xs, Y1, "r-", label = self.velocityInterval[0])
        plt.plot(Xs, Y2, "b-", label = self.velocityInterval[1])
        plt.plot(Xs, Y3, "g-", label = self.velocityInterval[2])
        plt.plot(Xs, Y4, "y-", label = self.velocityInterval[3])
        plt.plot(Xs, Y5, "v-", label = self.velocityInterval[4])
        plt.title(" Energy Consumption Vs PumpEfficiency")
        plt.xlabel("Efficiency")
        plt.ylabel("Energy consumption")
        plt.legend()
        plt.savefig('Energy Consumption Vs PumpEfficiency')
        plt.close()
        
    def EnergyConsumptionAndDiameter(self,circuit):
        TEnergy = np.zeros((5,30))
        ActualEnergy = []
        VelocityInterval = np.zeros((30,5))
        self.efficiency = self.PumpEfficiency(circuit)
        self.diameter = np.linspace(0.7,1,30)
        self.valveState = self.GetValveStatus(circuit)
        self.filterState = self.GetFilterStatus(circuit)
        for i in range (0, len(self.diameter)):
            velocities = self.MaximumVelocity(self.diameter[i])
            VelocityInterval[i] = velocities
        self.VelocitiesTaken = VelocityInterval[29]
        for i in range (0, len(self.diameter)):
            for j in range (0,5,1):
                TE = self.CalculateTheoreticalEnergy(circuit, self.VelocitiesTaken[j],  self.diameter[i], self.height, self.valveState, self.filterState) 
                TEnergy[j][i] = TE
        for i in range(0, len(TEnergy)):
            TheoreticalEnergy = TEnergy[i]
            EnergyConsumed = TheoreticalEnergy/self.efficiency
            ActualEnergy.append(EnergyConsumed)

        
        Xs = np.linspace(0.7,1,30)
        
        Y1 = ActualEnergy[0]
        Y2 = ActualEnergy[1]
        Y3 = ActualEnergy[2]
        Y4 = ActualEnergy[3]
        Y5 = ActualEnergy[4]
        
        plt.plot(Xs, Y1, "r-", label = self.VelocitiesTaken[0])
        plt.plot(Xs, Y2, "b-", label = self.VelocitiesTaken[1])
        plt.plot(Xs, Y3, "g-", label = self.VelocitiesTaken[2])
        plt.plot(Xs, Y4, "y-", label = self.VelocitiesTaken[3])
        plt.plot(Xs, Y5, "v-", label = self.VelocitiesTaken[4])
        plt.title(" Energy Consumption Vs Diameter")
        plt.xlabel("Diameter")
        plt.ylabel("Energy consumption")
        plt.legend()
        plt.savefig('Energy Consumption Vs Diameter')
        plt.close()
        
        
    def EnergyConsumptionAndHeight(self,circuit):
        TEnergy = np.zeros((5,20))
        ActualEnergy = []
        self.height = np.linspace(1,10,20)
        self.diameter = self.testCircuit[1].diameter
        self.velocityInterval = self.MaximumVelocity(self.diameter)
        self.valveState = self.GetValveStatus(circuit)
        self.filterState = self.GetFilterStatus(circuit)
        efficiency = self.PumpEfficiency(circuit)
        for i in range (0, len(self.height)):
            for j in range (0,len(self.velocityInterval)):
                TE = self.CalculateTheoreticalEnergy(circuit, self.velocityInterval[j],  self.diameter, self.height[i], self.valveState, self.filterState)
                TEnergy[j] = TE
        for i in range(0, len(TEnergy)):
            TheoreticalEnergy = TEnergy[i]
            EnergyConsumed = TheoreticalEnergy/efficiency
            ActualEnergy.append(EnergyConsumed)   
        Xs = np.linspace(1,10,20)
        Y1 = ActualEnergy[0]
        Y2 = ActualEnergy[1]
        Y3 = ActualEnergy[2]
        Y4 = ActualEnergy[3]
        Y5 = ActualEnergy[4]
        plt.plot(Xs, Y1, "r-", label = self.velocityInterval[0])
        plt.plot(Xs, Y2, "b-", label = self.velocityInterval[1])
        plt.plot(Xs, Y3, "g-", label = self.velocityInterval[2])
        plt.plot(Xs, Y4, "y-", label = self.velocityInterval[3])
        plt.plot(Xs, Y5, "v-", label = self.velocityInterval[4])
        plt.title(" Energy Consumption Vs Height")
        plt.xlabel("Height")
        plt.ylabel("Energy consumption")
        plt.legend()
        plt.savefig('Energy Consumption Vs Height')
        plt.close()
        
    def EnergyConsumptoionAndValves(self, circuit):
        TEnergy = np.zeros((5,20))
        ActualEnergy = []
        self.diameter = self.testCircuit[1].diameter
        self.velocityInterval = self.MaximumVelocity(self.diameter)
        self.stateInterval = np.linspace(0.5, 1.0, 20)
        self.height = self.TotalHeight(circuit)
        self.filterState = self.GetFilterStatus(circuit)
        efficiency = self.PumpEfficiency(circuit)
        for j in range (0,len(self.velocityInterval)):
            TE = self.CalculateTheoreticalEnergy(circuit, self.velocityInterval[j],  self.diameter, self.height, self.stateInterval, self.filterState)
            TEnergy[j] = TE
        for i in range(0, len(TEnergy)):
            TheoreticalEnergy = TEnergy[i]
            EnergyConsumed = TheoreticalEnergy/efficiency
            ActualEnergy.append(EnergyConsumed) 
        Xs = np.linspace(0.5, 1.0, 20)
        Y1 = ActualEnergy[0]
        Y2 = ActualEnergy[1]
        Y3 = ActualEnergy[2]
        Y4 = ActualEnergy[3]
        Y5 = ActualEnergy[4]
        plt.plot(Xs, Y1, "r-", label = self.velocityInterval[0])
        plt.plot(Xs, Y2, "b-", label = self.velocityInterval[1])
        plt.plot(Xs, Y3, "g-", label = self.velocityInterval[2])
        plt.plot(Xs, Y4, "y-", label = self.velocityInterval[3])
        plt.plot(Xs, Y5, "v-", label = self.velocityInterval[4])
        plt.title(" Energy Consumption Vs Valve")
        plt.xlabel("Valve")
        plt.ylabel("Energy consumption")
        plt.legend()
        plt.savefig('Energy Consumption Vs Valve')
        plt.close()
        
    def EnergyConsumptoionAndFilter(self, circuit):
        TEnergy = np.zeros((5,20))
        ActualEnergy = []
        self.diameter = self.testCircuit[1].diameter
        self.velocityInterval = self.MaximumVelocity(self.diameter)
        self.stateInterval = np.linspace(0.5, 1.0, 20)
        self.height = self.TotalHeight(circuit)
        self.valveState = self.GetValveStatus(circuit)
        efficiency = self.PumpEfficiency(circuit)
        for j in range (0,len(self.velocityInterval)):
            TE = self.CalculateTheoreticalEnergy(circuit, self.velocityInterval[j],  self.diameter, self.height, self.stateInterval, self.filterState)
            TEnergy[j] = TE
        for i in range(0, len(TEnergy)):
            TheoreticalEnergy = TEnergy[i]
            EnergyConsumed = TheoreticalEnergy/efficiency
            ActualEnergy.append(EnergyConsumed) 
        Xs = np.linspace(0.5, 1.0, 20)
        Y1 = ActualEnergy[0]
        Y2 = ActualEnergy[1]
        Y3 = ActualEnergy[2]
        Y4 = ActualEnergy[3]
        Y5 = ActualEnergy[4]
        plt.plot(Xs, Y1, "r-", label = self.velocityInterval[0])
        plt.plot(Xs, Y2, "b-", label = self.velocityInterval[1])
        plt.plot(Xs, Y3, "g-", label = self.velocityInterval[2])
        plt.plot(Xs, Y4, "y-", label = self.velocityInterval[3])
        plt.plot(Xs, Y5, "v-", label = self.velocityInterval[4])
        plt.title(" Energy Consumption Vs Filter")
        plt.xlabel("Filter")
        plt.ylabel("Energy consumption")
        plt.legend()
        plt.savefig('Energy Consumption Vs Filter')
        plt.close()        
        
                    
        
        
        
        