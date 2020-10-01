# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 01:30:25 2020

@author: krish
"""

# =============================================================================
# Required Modules
# =============================================================================

import random
import math

# =============================================================================
# Initialize Units
# =============================================================================

class Unit():
    
    def __init__(self, name, failureRate, repairRate, capacity):
        self.name = name
        self.failureRate = failureRate
        self.repairRate = repairRate
        self.capacity = capacity
        self.working = True
        
    def Transition(self):
        if self.working:
            self.working = False
        else:
            self.working = True
            
    def DrawDuration(self):
        z = random.random()
        duration = 0
        rate = 0
        if self.working:
            rate = self.failureRate
        else:
            rate = self.repairRate
        duration = -math.log(z)/rate
        return duration
    
    def GetCapacity(self):
        return self.capacity
    
# =============================================================================
# Initialize Markov Chains    
# =============================================================================

class MarkovChain():
    def __init__(self, name ):
        self.name = name
        self.units = []
  
    def LookForUnit(self, name):
        for item in self.units:
            if item.name == name:
                return item
        return None
    
    def AddUnit(self, name, failureRate, repairRate, capacity):
        unit = self.LookForUnit(name)
        if unit != None:
            return unit
        unit = Unit(name, failureRate, repairRate, capacity)
        self.units.append(unit)
    
    def GetUnits(self):
        return self.units
        
# =============================================================================
# Initialize Markov Systems 
# =============================================================================

class MarkovSystem:
    def __init__(self):
        self.markovChains = []
        
    def LookForMarkovChain(self, name):
        for item in self.markovChains:
            if item.name == name:
                return item
        return None
        
    def AddUnit(self, name, chain, failureRate, repairRate, capacity):
        markovChain = self.LookForMarkovChain(chain)
        if markovChain == None:
            markovChain = MarkovChain(chain)
            self.markovChains.append(markovChain)
        markovChain.AddUnit(name, failureRate, repairRate, capacity)
      
    def GetMarkovChains(self):
        return self.markovChains
    
    def GetUnits(self):
        units = []
        for item in self.markovChains:
            for unit in item.GetUnits():
                units.append(unit)
        return units
    
    def GetFacilityCapacity(self):
        Capacity = []         
        for item in self.markovChains:
            chainCapacity = 0
            for unit in item.GetUnits():
                if unit.working:
                    chainCapacity += unit.GetCapacity()
                if chainCapacity > 100:
                    chainCapacity = 100
            Capacity.append(chainCapacity)
        facilityCapacity = min(Capacity)
        return facilityCapacity

    
    
    