# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 18:18:44 2020

@author: krish
"""
import sys

#Parents

class Elements:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        
    def GetName(self):
        return self.name
    
    def GetType(self):
        return self.type

#Tank

class Tank(Elements):
    def __init__(self, name):
        Elements.__init__(self, name, "tank")

#Pipe
class Pipe(Elements):
    def __init__(self,name,length,diameter,angle)    :
        Elements.__init__(self, name, "pipe")
        self.diameter = diameter
        self.length = length
        self.angle = angle
    
    def GetLength(self):
        return self.length
        
    def GetDiameter(self):
        return self.diameter
    
    def GetAngle(self):
        return self.angle

#Bends
class Bend(Elements):
    def __init__(self,name,diameter):
        Elements.__init__(self, name, "bend")
        self.diameter = diameter
        
    def GetDiameter(self):
        return self.diameter

#Pumps
class Pump(Elements):
    def __init__(self,name,efficiency):
        Elements.__init__(self, name, "pump")
        self.efficiency = efficiency
        
    def GetEfficiency(self):
        return self.efficiency

#Valves
class Valve(Elements):
    def __init__(self,name,status):
        Elements.__init__(self, name, "valve")
        self.status = status
        
    def GetStatus(self):
        return self.status

#Filters
class Filter(Elements):
    def __init__(self,name,status):
        Elements.__init__(self, name, "filter")
        self.status = status
     
    def GetStatus(self):
        return self.status

#Circuit
class Circuit():
    def __init__(self):
        self.type = "Circuit"
        self.circuit = []
        
    def GetAllElements(self):
        return self.circuit
        
    def AddElement(self, element):
        self.circuit.append(element)
    
    def GetElement(self,index):
        return self.circuit.index

    def NewTank(self,name):
        tank = Tank(name)
        self.AddElement(tank)
        return tank
    
    def NewPipe(self,name,length,diameter,angle):
        pipe = Pipe(name,length,diameter,angle)
        self.AddElement(pipe)
        return pipe
    
    def NewPump(self,name,efficiency):
        pump = Pump(name,efficiency)
        self.AddElement(pump)
        return pump
    
    def NewValve(self,name,status):
        valve = Valve(name,status)
        self.AddElement(valve)
        return valve
    
    def NewFilter(self,name,status):
        filter = Filter(name,status)
        self.AddElement(filter)
        return filter
    
    def NewBend(self,name,diameter):
        bend = Bend(name,diameter)
        self.AddElement(bend)
        return bend              

