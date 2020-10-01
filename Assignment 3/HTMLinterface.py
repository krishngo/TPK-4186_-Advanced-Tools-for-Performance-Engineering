# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 03:47:12 2020

@author: krish
"""

# =============================================================================
# Required modules
# =============================================================================
import re
import sys
# =============================================================================
# HTML serializer
# =============================================================================
class HTMLSerializer:
    def __init__(self):
        self.indentation = "\t"
        self.depth = 0
        
    def SerializeStatistics(self, statistics):
        result = self.SerializeOpenTag('table id="Table"')
        self.depth += 1
        result += self.SerializeStatisticsHeader()
        for element in statistics:
            result += self.SerializeOpenTag('tr')
            self.depth += 1
            result += self.SerializeOpenTag("td")
            result += str(element)
            result += self.SerializeCloseTag("td")
            result += self.SerializeOpenTag("td")
            result += f'{statistics[element]}'
            result += self.SerializeCloseTag("td")
        self.depth -= 1
        result += self.SerializeCloseTag("table")
        return result  

    def SerializeStatisticsHeader(self):
        result = self.SerializeOpenTag("tr")
        self.depth += 1
        result += self.SerializeOpenTag("th")
        result += 'Assessed Statistic'
        result += self.SerializeCloseTag("th")
        result += self.SerializeOpenTag("th")
        result += 'Found Value'
        result += self.SerializeCloseTag("th")
        self.depth -= 1
        result += self.SerializeCloseTag("tr")
        return result
    
    def SerializeAttributeValue(self, value):
        return "{0:.2f}".format(value)
        
    def SerializeIndentation(self):
        result = ""
        for de in range(0, self.depth):
          result += self.indentation
        return result
    
    def SerializeOpenTag(self, name):
        return self.SerializeIndentation() + "<" + name + ">\n"
    
    def SerializeCloseTag(self, name):
        return self.SerializeIndentation() + "</" + name + ">\n" 

# =============================================================================
# HTML maker    
# =============================================================================

class HTMLCreator:
    def __init__(self):
        self.serializer = HTMLSerializer()
        
    def ExportHTMLFormat(self, templateFile, targetFile, statistics):
        try:
            templateFile = open(templateFile, 'r')
        except:
            sys.stderr.write('Unable to open file "%s"\n' % templateFile)
            sys.stderr.flush()
            return 1
        try:
            targetFile = open(targetFile, 'w')
        except:
            sys.stderr.write('Unable to open file "%s"\n' % targetFile)
            sys.stderr.flush()
            templateFile.close()
            return 1
        self.PrintReport( templateFile, targetFile, statistics)
        templateFile.close()
        targetFile.flush()
        targetFile.close()
        return 0
    
    def PrintReport(self, templateFile, targetFile, statistics):
        for line in templateFile:
            line = line.rstrip()
            if re.search(r'__STATISTICS__', line):
                line = re.sub(r'__STATISTICS__', self.serializer.SerializeStatistics(statistics), line)
            targetFile.write(line + '\n') 
    
    
    
    
    
    
    
    
    
    