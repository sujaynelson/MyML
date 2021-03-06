# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 12:26:30 2019

@author: pmaddala
"""

import numpy as np
from enum import Enum
import math
import matplotlib.pyplot as plt
import random

class Cost(Enum):
    MSE = 1
    MAE = 2
    
class Optimizer(Enum):
    SGD = 1
    BATCH_GRAD = 2
    MINI_BATCH_GRAD = 3
    
class Regularization(Enum):
    LASSO = 1
    RIDGE = 2
    
class LinearRegression:
    def __init__(self,x,y,alpha=0.01,cost=Cost.MSE,Lambda=0,optimizer=Optimizer.BATCH_GRAD,regularization=None):
        self.input = x
        t = []
        #Adding dimension X[0]=1, to accomodate bias
        for i in range(len(x)):
            t.append(np.insert(x[i],0,1))
        self.x = np.array(t)  
        self.y = y
        self.alpha = alpha
        self.coef = np.random.random(1+len(x[0]))
        self.cost = cost
        self.errors = []
        self.optimizer = optimizer
        #Regularization parameter
        self.Lambda = Lambda
        self.regularization = regularization
        
    def train(self,iterations=100):
        if self.optimizer == Optimizer.BATCH_GRAD:
            for i in range(iterations):
                #Find error and add it to the list, just for display purposes
                error = self.getError(self.x,self.y)
                self.errors.append(error)
                self.coef = self.coef - self.alpha*self.diff(self.x,self.y)
            
        if self.optimizer == Optimizer.SGD:
            for i in range(iterations):
                error = self.getError(self.x,self.y)
                self.errors.append(error)
                sample = random.randint(0,len(self.x)-1)
                self.coef = self.coef - self.alpha*self.diff(self.x[sample],self.y[sample])
                
    def train_tolerannce(self,e=0.05):
        error = self.getError()
        self.errors.append(error)
        prev = error
        while True:
            self.coef = self.coef - self.alpha*self.diff()
            terr = self.getError()
            self.errors.append(terr)
            if abs(terr-prev)<=e:
                break
            prev = terr
            
        
    def getError(self,x,y):
        if self.cost == Cost.MSE:
            error = 0
            for i in range(len(x)):
                error = error + (y[i]-np.dot(self.coef,x[i]))**2
            return math.sqrt(error)/len(x)
        if self.cost == Cost.MAE:
            error = 0
            for i in range(len(x)):
                error = error + abs(self.y[i]-np.dot(self.coef,self.x[i]))
            return error
                
    def __regularize__(self,weight):
        if self.regularization==None:
            return 0
        if self.regularization==Regularization.LASSO:
            if weight<0:
                return -self.Lambda
            return self.Lambda
        if self.regularization==Regularization.RIDGE:
            return self.Lambda * 2 * weight
        return None
        
    def diff(self,x,y):
        if self.optimizer == Optimizer.BATCH_GRAD:
            tcoef = []
            for c in range(len(self.coef)):
                const = 0
                for i in range(len(x)):
                    const = const +(-2/len(x))* (self.y[i]-np.dot(self.coef,self.x[i]))*(self.x[i][c]) 
                tcoef.append(const + self.__regularize__(self.coef[c]))
            tcoef = np.array(tcoef)
            return tcoef
        
        if self.optimizer == Optimizer.SGD:
            tcoef = []
            for c in range(len(self.coef)):
                const = (-2*x[c])*(y-np.dot(self.coef,x)) + self.__regularize__(self.coef[c])
                tcoef.append(const)
            return np.array(tcoef)
            
            
    def predict(self,x_new):        
        return self.coef*np.insert(x_new,0,1)
        
    def plotInput(self):
        plt.scatter(self.input,self.y)
        plt.plot(np.linspace(0,10,100),self.coef[1]*np.linspace(0,10,100) + self.coef[0])
        
    def plot_errors(self):
        plt.plot(range(len(self.errors)),self.errors)
        
        
if __name__ == '__main__':
    x = []  
    y = []
    for i in range(10):
        x.append([i])
        y.append(3*i-2+np.random.randint(-2,3))
        
    x = np.array(x)
    y = np.array(y)
    l = LinearRegression(x,y,cost=Cost.MSE,Lambda=1,optimizer=Optimizer.SGD,regularization=Regularization.RIDGE)
    #l = LinearRegression(x,y,cost=Cost.MSE,Lambda=0,optimizer=Optimizer.SGD)
    l.train(iterations=1000)
    l.plotInput()
    l.plot_errors()