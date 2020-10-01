# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 01:11:12 2020

@author: krish
"""

# =============================================================================
# Imported modules
# =============================================================================

import sys
import DataStructure
import MonteCarloSimulation
import XMLInterface
import numpy as np
import sklearn

calculator = MonteCarloSimulation.Calculator()

# =============================================================================
#Classification
# =============================================================================

class Classifier:
    def __init__(self):
        pass
       
    def CreateSample(self, noOfTrials, diagram, gateName, maximumDuration):
        totalDuration = np.zeros(noOfTrials)
        points = np.zeros((noOfTrials,10))
        labels = np.zeros(noOfTrials)     
        for trial in range(0,noOfTrials):
            totalDuration[trial]= calculator.CalculateTotalDuration(diagram)
            gateCompletionDate = calculator.CompletionDatesOfNodesBeforeGivenGate(diagram, gateName) ###
            for index in range(0,len(gateCompletionDate)):
                points[trial][index] = gateCompletionDate[index]
            if totalDuration[trial] < maximumDuration:
                labels[trial] = 0
            else:
                labels[trial] = 1
        return (points,labels)
    
    def ClassificationTemplate(self, model, noOfTrials, diagram, gateName, maximumDate ):
        (trainingPoints, trainingLabels) = self.CreateSample(noOfTrials, diagram, gateName, maximumDate)
        model.fit(trainingPoints, trainingLabels)
        (testPoints, testLabels) = self.CreateSample(noOfTrials, diagram, gateName, maximumDate)
        predictedLabels = model.predict(testPoints)
        classificationAccuracy = self.CalculateAccuracy(predictedLabels, testLabels)
        return classificationAccuracy
        
    def CalculateAccuracy(self, predictedLabels, testLabels):
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(testLabels, predictedLabels)
        return accuracy
    
    def LogisticRegression(self, noOfTrials, diagram, gateName, maximumDate):
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
        return self.ClassificationTemplate(model, noOfTrials, diagram, gateName, maximumDate )
    
    def StochasticGradientDescent(self, noOfTrials, diagram, gateName, maximumDate):
        from sklearn.linear_model import SGDClassifier
        model = SGDClassifier()
        return self.ClassificationTemplate(model, noOfTrials, diagram, gateName, maximumDate )
    
    def MultiLayerPerceptron(self, noOfTrials, diagram, gateName, maximumDate):
        from sklearn.neural_network import MLPClassifier
        model = MLPClassifier()
        return self.ClassificationTemplate(model, noOfTrials, diagram, gateName, maximumDate )
    
    def AccuracyOfClassificationMethods(self, noOfTrials, diagram, gateName):
        maximumDates = [96,102,108]
        classificationAccuracies = dict()
        logisticRegressionAccuracies = []
        stochasticGradientDescentAccuracies = []
        multiLayerPerceptronAccuracies = []
        for date in maximumDates:
            logisticRegressionAccuracy = self.LogisticRegression(noOfTrials, diagram,  "MidProject",date)
            logisticRegressionAccuracies.append(logisticRegressionAccuracy)
            stochasticGradientDescentAccuracy = self.StochasticGradientDescent(noOfTrials, diagram,  "MidProject",date)
            stochasticGradientDescentAccuracies.append(stochasticGradientDescentAccuracy)
            multiLayerPerceptronAccuracy = self.MultiLayerPerceptron(noOfTrials, diagram,  "MidProject",date)
            multiLayerPerceptronAccuracies.append(multiLayerPerceptronAccuracy)
        classificationAccuracies["Logistic Regression"] = logisticRegressionAccuracies
        classificationAccuracies["Stochastic Gradient Descent"] = stochasticGradientDescentAccuracies
        classificationAccuracies["Multi-Layer Perceptron"] = multiLayerPerceptronAccuracies
        return classificationAccuracies
                  
    
    







