# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 14:01:47 2020

@author: krish
"""

import xml.dom.minidom
import sys
import Core

class XMLParser:
    def ImportCircuitXMLFormat(self, circuit, fileName):
        try:
            xmlDocument = xml.dom.minidom.parse(fileName)
        except:
            sys.stderr.write('Error while loading file "%s"\n' % fileName)
            sys.stderr.flush()
            return 1
        error = self.DownloadCircuit(circuit, xmlDocument)
        return error
    
    def DownloadCircuit(self, circuit, xmlDocument):
        xmlElement = xmlDocument.documentElement
        xmlNode = xmlElement.firstChild
        error = 0
        while xmlNode != None:
            if xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'tank':
                error = self.DownloadTank(circuit, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'pipe':
                error = self.DownloadPipe(circuit, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'pump':
                error = self.DownloadPump(circuit, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'bend':
                error = self.DownloadBend(circuit, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'filter':
                error = self.DownloadFilter(circuit, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'valve':
                error = self.DownloadValve(circuit, xmlNode)
            elif error != 0:
                break                
            xmlNode = xmlNode.nextSibling
        return error
    
    def DownloadTank(self, circuit, xmlElement):
        name = xmlElement.getAttribute('name')
        if name == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        circuit.NewTank(name)
        return 0
    
    def DownloadPipe(self, circuit, xmlElement):
        name = xmlElement.getAttribute('name')
        length = xmlElement.getAttribute('length')
        diameter = xmlElement.getAttribute('diameter')
        angle = xmlElement.getAttribute('angle')
        if name == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        circuit.NewPipe(name, float(length), float(diameter), float(angle))
        return 0
    
    def DownloadPump(self, circuit, xmlElement):
        name = xmlElement.getAttribute('name')
        efficiency = xmlElement.getAttribute('efficiency')
        if name == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        circuit.NewPump(name, float(efficiency))
        return 0
    
    def DownloadBend(self, circuit, xmlElement):
        name = xmlElement.getAttribute('name')
        diameter = xmlElement.getAttribute('diameter')
        if name == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        circuit.NewBend(name, float(diameter))
        return 0
    
    def DownloadFilter(self, circuit, xmlElement):
        name = xmlElement.getAttribute('name')
        filterState = xmlElement.getAttribute('cleanliness')
        if name == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        circuit.NewFilter(name, float(filterState))
        return 0
    
    def DownloadValve(self, circuit, xmlElement):
        name = xmlElement.getAttribute('name')
        valveState = xmlElement.getAttribute('opening')
        if name == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        circuit.NewValve(name, float(valveState))
        return 0
     
        
