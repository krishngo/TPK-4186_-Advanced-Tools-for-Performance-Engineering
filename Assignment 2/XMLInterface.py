# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 01:37:14 2020

@author: krish
"""

# =============================================================================
# Required modules
# =============================================================================

import sys
import DataStructure
import xml.dom.minidom

# =============================================================================
# Parser
# =============================================================================

class XMLParser:
    
    def ImportDiagramXMLFormat(self, fileName, diagram):
        try:
            xmlDocument = xml.dom.minidom.parse(fileName)
        except:
            sys.stderr.write('Error while loading file "%s"\n' % fileName)
            sys.stderr.flush()
            return 1
        error = self.DownloadDiagram(diagram, xmlDocument)
        return error
    
    def DownloadDiagram(self, diagram, xmlDocument):
        xmlRootElement = xmlDocument.documentElement
        if xmlRootElement.tagName.capitalize()!="Project":
            sys.stderr.write('An element "project" was expected\n')
            sys.stderr.flush()
            return 1
        projectName = xmlRootElement.getAttribute('name')
        if projectName==None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        xmlNode = xmlRootElement.firstChild 
        error = 0
        while xmlNode != None:
            if xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'gate':
                error = self.DownloadGate(diagram, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'lane':
                error = self.DownloadLane(diagram, xmlNode)
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'precedence-constraint':
                error = self.DownloadPrecedenceConstraint(diagram, xmlNode)
            elif error != 0:
                break
            xmlNode = xmlNode.nextSibling
        return error

    def DownloadGate(self, diagram, xmlElement):
        gateName = xmlElement.getAttribute('name')
        if gateName == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        diagram.NewGate(gateName)
        return 0
    
    def DownloadLane(self, diagram, xmlElement):
        laneName = xmlElement.getAttribute('name')
        xmlNode = xmlElement.firstChild
        laneElements = dict()
        error = 0
        while xmlNode != None:
            if xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'task':
                laneElement = self.DownloadTask(diagram, xmlNode)
                error = laneElement[0]
                laneElements[laneElement[1]] = diagram.NewTask(laneElement[1], laneElement[2], laneElement[3])
            elif xmlNode.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and xmlNode.tagName == 'precedence-constraint':
                error = self.DownloadPrecedenceConstraint(diagram, xmlNode)
            elif error != 0:
                break
            xmlNode = xmlNode.nextSibling
        diagram.NewLane(laneName, laneElements)
        return 0
    
    def DownloadTask(self, diagram, xmlElement):
        taskName = xmlElement.getAttribute('name')
        minimumDuration = xmlElement.getAttribute('minimum-duration')
        maximumDuration = xmlElement.getAttribute('maximum-duration')
        if taskName == None:
            sys.stderr.write('An attribute "name" was expected\n')
            sys.stderr.flush()
            return 1
        diagram.NewTask(taskName, minimumDuration, maximumDuration)
        return [0, taskName, float(minimumDuration), float(maximumDuration)]

    def DownloadPrecedenceConstraint(self, diagram, xmlElement):
        sourceNode = xmlElement.getAttribute('source')
        targetNode = xmlElement.getAttribute('target')
        if sourceNode == None or targetNode == None:
            sys.stderr.write('Attributes "source" and "target" was expected\n')
            sys.stderr.flush()
            return 1
        diagram.NewPrecedenceConstraint(sourceNode, targetNode)
        return 0




























    