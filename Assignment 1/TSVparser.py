# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 14:16:23 2020

@author: krish
"""
import sys

class TSVParser:
  def __init__(self):
    self.separator = "\t"
  
  def ImportFile(self, circuit, fileName):
    try:
      file = open(fileName, "r")
    except:
      sys.stderr.write("Unable to open file " + fileName + "\n")
      sys.exit()
    header = True
    for line in file:
      if header:
        header = False
      else:
        line = line.rstrip()
        tokens = line.split(self.separator)
        type = tokens[0].lower()
        if type == "tank":
            name = tokens[1]
            circuit.NewTank(name)
        elif type == "pipe":
            name = tokens[1]
            length = float(tokens[2])
            diameter = float(tokens[3])
            angle = float(tokens[4])
            circuit.NewPipe(name,length,diameter,angle)
        elif type == "pump":
            name = tokens[1]
            efficiency = float(tokens[2])
            circuit.NewPump(name,efficiency)       
        elif type == "valve":
            name = tokens[1]
            status = float(tokens[2])
            circuit.NewValve(name,status)
        elif type == "filter":
            name = tokens[1]
            status = float(tokens[2])
            circuit.NewFilter(name,status)
        elif type == "bend":
            name = tokens[1]
            diameter = float(tokens[2])
            circuit.NewBend(name,diameter)  
    file.flush()
    file.close()       
 