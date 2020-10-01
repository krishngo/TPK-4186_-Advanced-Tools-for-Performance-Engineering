# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:53:12 2020

@author: krish
"""
from Core import *
import sys


class SequenceChecker():
    def __init__(self,circuit):
       self.testCircuit = circuit.GetAllElements()
       self.type = []
       for element in circuit.GetAllElements():
            self.type.append(element.GetType())
              
    def Checker(self,circuit):       
        self.Condition1(type)
        self.Condition2(type)
        self.Condition3(circuit)
        self.Condition4(circuit)
        self.Condition5(circuit)
        self.Condition6(circuit)
        self.Condition7(circuit)
        self.Condition8(circuit)
        self.Condition9(circuit)
        self.Condition10(circuit)
        return True

        
    def Condition1(self,type):
        if self.type[0] and self.type[-1] == "tank":
            return True
        else:
            sys.exit("First and last elements are not tanks")

    def Condition2(self,type):
        count = 0
        for item in self.type:
            if item == "tank":
                count += 1
        if count == 2:
            return True
        else:
            sys.exit("More than two tanks")
        
    def Condition3(self,circuit):
        if self.testCircuit[1].type == "pipe":
            if self.testCircuit[1].angle == 0:
                return True
            else:
                sys.exit("Second element not a horizontal pipe")
        else:
            sys.exit("Second element not a pipe")
    
    def Condition4(self,circuit):
        count = 0
        for item in self.type:
            if item == "pump":
                count += 1
        if count >1:
            sys.exit("More than one pump")
        else:
            return True
                
    
    def Condition5(self,circuit):
        stdDiameter = self.testCircuit[1].diameter
        for element in self.testCircuit:
            if element.type == "pipe" or element.type == "bend":
                if element.diameter != stdDiameter:
                    sys.exit("All pipes and bend does not have same inside diameter")
        return True
    
    def Condition6(self,circuit):
        test = True
        for element in self.testCircuit:
            if element.type == "pipe":
                index = self.testCircuit.index(element)
                nxt = index + 1
                if self.testCircuit[nxt].type == "pipe":    
                    if self.testCircuit[nxt].angle != self.testCircuit[index].angle:
                        sys.exit("Succeeding pipes do not have the same angle")
        return test
    
    def Condition7(self,circuit):
        if self.type[-2] != "bend":
            sys.exit("The element before tank is not a bend") #***
        for i in range(0,len(self.type)-2):
            if self.testCircuit[i].type == "bend":
                if self.testCircuit[i+1].type == "pipe" and self.testCircuit[i-1].type == "pipe":
                    if self.testCircuit[i+1].angle == self.testCircuit[i-1].angle:
                        sys.exit("Bends should be preceeded and succeeded by pipes at 90 degrees to each other")
                else:
                    sys.exit("Bends should be preceeded and succeeded by pipes")
        return True
    
    def Condition8(self,circuit):
            test = True
            for element in self.testCircuit:
                if element.type == "pump":
                    index = self.testCircuit.index(element)
                    nxt = index + 1
                    prev = index - 1
                    if self.testCircuit[nxt].type != "pipe" or self.testCircuit[prev].type != "pipe":
                        sys.exit("Pumps must be preceeded and succeeded by pipes")
                    if self.testCircuit[nxt].angle != 0 or self.testCircuit[prev].angle != 0:
                        sys.exit("Pumps must be preceeded and succeeded by horizontal pipes")
            return test    
    
        
    def Condition9(self,circuit):
        test = True
        for element in self.testCircuit:
            if element.type == "filter":
                index = self.testCircuit.index(element)
                nxt = index + 1
                prev = index - 1
                if self.testCircuit[nxt].type != "pipe" or self.testCircuit[prev].type != "pipe":
                    sys.exit("Filters must be preceeded and succeeded by pipes")
                if self.testCircuit[nxt].angle != 0 or self.testCircuit[prev].angle != 0:
                    sys.exit("Filters must be preceeded and succeeded by horizontal pipes")
        return test
    
    def Condition10(self,circuit):
        test = True
        for element in self.testCircuit:
            if element.type == "valve":
                index = self.testCircuit.index(element)
                nxt = index + 1
                prev = index - 1
                if self.testCircuit[nxt].type != "pipe" or self.testCircuit[prev].type != "pipe":
                    sys.exit("Valve must be preceeded and succeeded by pipes")
                if self.testCircuit[nxt].angle != self.testCircuit[prev].angle:
                    sys.exit("Valve must be preceeded and succeeded by pipes of same angle")
        return test
    
        
        
    

  

                
                    
       
        
        
        
        
        
        
        
        