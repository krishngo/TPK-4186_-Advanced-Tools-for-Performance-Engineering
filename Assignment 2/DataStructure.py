# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:35:54 2020

@author: krish
"""
# =============================================================================
# Modules imported
# =============================================================================

import sys

# =============================================================================
# Nodes 
# =============================================================================

class Node:
   GATE = 0
   TASK = 1
    
   def __init__(self, type, name):
        self.type = type
        self.name = name
        self.startDate = -1
        self.completionDate = -1
        self.duration = 0
        self.predecessors = []
        self.successors = []

   def GetName(self):
        return self.name
    
   def GetType(self):
        return self.type

   def AddPredecessor(self, node):
        self.predecessors.append(node)
        
   def AddSuccessor(self, node):
        self.successors.append(node)
        
   def CollectAscendants(self, ascendants):
        if self in ascendants:
            return
        ascendants.append(self)
        for predecessor in self.predecessors:
            predecessor.CollectAscendants(ascendants)
            
   def CollectDescendants(self, descendants):
        if self in descendants:
            return
        descendants.append(self)
        for successor in self.successors:
            successor.CollectDescendants(descendants)
            
# =============================================================================
# Gates            
# =============================================================================
            
class Gate(Node):
    def __init__(self, name):
         Node.__init__(self, Node.GATE, name) 

# =============================================================================
# Task           
# =============================================================================
            
class Task(Node):
    def __init__(self, name, minimumDuration, maximumDuration):
        Node.__init__(self, Node.TASK, name)
        self.minDuration = minimumDuration
        self.maxDuration = maximumDuration        

# =============================================================================
# Diagrams
# =============================================================================
        
class Diagram:
    def __init__(self):
        self.nodes = dict()
        self.lanes = dict()
            
    def LookForNode(self, name):
        return self.nodes.get(name, None)

    def GetNodes(self):
        return self.nodes.values()

    def NewGate(self, name):
        gate = Gate(name)
        self.nodes[name] = gate
        return gate

    def NewLane(self, name, task):
        self.lanes[name] = task
        return task     

    def NewTask(self, name, minimumDuration, maximumDuration):
        task = Task(name, minimumDuration, maximumDuration)
        self.nodes[name] = task
        return task       

    def NewPrecedenceConstraint(self, sourceNode, targetNode):
        self.nodes[sourceNode].AddSuccessor(self.nodes[targetNode])
        self.nodes[targetNode].AddPredecessor(self.nodes[sourceNode])          
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            