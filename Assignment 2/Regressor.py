# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 01:55:43 2020

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
# Regression
# =============================================================================

class Regressor:
    def __init__(self):
        pass
    
    def CreateSample(self, noOfTrials, diagram, gateName):
        totalDuration = np.zeros(noOfTrials)
        points = np.zeros((noOfTrials,10))
        labels = np.zeros(noOfTrials)
        for trial in range(0,noOfTrials):
            totalDuration[trial]= calculator.CalculateTotalDuration(diagram)
            gateCompletionDate = calculator.CompletionDatesOfNodesBeforeGivenGate(diagram, gateName) ###
            for index in range(0,len(gateCompletionDate)):
                points[trial][index] = gateCompletionDate[index]
            labels[trial] = totalDuration[trial]
        return (points,labels)
    
    def RegressionTemplate(self, model, noOfTrials, diagram, gateName):
        (trainingPoints, trainingLabels) = self.CreateSample(noOfTrials, diagram, gateName)
        model.fit(trainingPoints, trainingLabels)
        (testPoints, testLabels) = self.CreateSample(noOfTrials, diagram, gateName)
        predictedLabels = model.predict(testPoints)
        regressionAccuracy = self.CalculateAccuracy(predictedLabels, testLabels)
        return regressionAccuracy

    def CalculateAccuracy (self, predictedLabels, testLabels):
        from sklearn.metrics import r2_score
        r2 = r2_score(testLabels, predictedLabels)
        return r2  

    def RidgeRegression(self, noOfTrials, diagram, gateName):
        from sklearn.linear_model import Ridge
        model = Ridge()
        return self.RegressionTemplate(model, noOfTrials, diagram, gateName)
    
    def LassoRegressor(self, noOfTrials, diagram, gateName):
        from sklearn import linear_model
        model = linear_model.Lasso()
        return self.RegressionTemplate(model, noOfTrials, diagram, gateName)
    
    def KNeighborsRegressor(self, noOfTrials, diagram, gateName):
        from sklearn.neighbors import KNeighborsRegressor
        model = KNeighborsRegressor(n_neighbors=5)
        return  self.RegressionTemplate(model, noOfTrials, diagram, gateName)
    
    def AccuracyOfRegressionMethods(self, noOfTrials, diagram, gateName):
        regressionAccuracies = dict()
        ridgeRegressionAccuracy = self.RidgeRegression(noOfTrials, diagram,  "MidProject")
        LassoRegressorAccuracy = self.LassoRegressor(noOfTrials, diagram,  "MidProject")
        KNeighborsRegressorAccuracy = self.KNeighborsRegressor(noOfTrials, diagram,  "MidProject")
        regressionAccuracies["Ridge Regression"] = ridgeRegressionAccuracy
        regressionAccuracies["Lasso regression"] = LassoRegressorAccuracy
        regressionAccuracies["K-Neighbours Regressor"] = KNeighborsRegressorAccuracy
        return regressionAccuracies

        



