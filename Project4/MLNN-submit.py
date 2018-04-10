# -*- coding: utf-8 -*-
"""
Created on Thu Dec 07 22:02:27 2017

@author: Mai Tian
"""

from __future__ import division
import math
import random
import pandas as pd

flowerLables = {0:'Iris-setosa', 1:'Iris-versicolor', 2:'Iris-virginica'}
random.seed(0)

# generate random number at [a, b)
def rand(a, b):
    return (b-a)*random.random() + a

# generate matrix with I * J
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# activation functions
def activate(name, x):
    if name == "sigmoid":
        return 1.0/(1.0+math.exp(-x))
    if name == "tanh":
        return math.tanh(x)
    if name == "Relu":
        return max(0, x)

# derivation for activation functions
def derivative(name, y):
    if name == "sigmoid":
        return y*(1-y)
    if name == "tanh":
        return 1.0 - y**2
    
class NN:
    
    def __init__(self, ni, nh, no):
        # number of nodes for input, hidden and output layers
        self.ni = ni + 1 # for bias node
        self.nh = nh
        self.no = no

        # activate all nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # weight matrix initialization
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # randomization
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # momentum matrix initialization
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs, act_func):
        
        if len(inputs) != self.ni-1:
            raise ValueError('Inconsistent with the node number of input layer!')

        # input layer activation
        for i in range(self.ni-1):
            self.ai[i] = inputs[i]

        # hidden layer activation
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = activate(act_func, sum)

        # output layer activation
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = activate(act_func, sum)

        return self.ao[:]

    def backPropagate(self, targets, act_func, N, M):

        # error in output layer
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = derivative(act_func, self.ao[k]) * error

        # error in hidden layer
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = derivative(act_func, self.ah[j]) * error

        # update weights between hidden and output layer
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # update weights between hidden and input layer
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # loss function and error
        error = 0.0
        error += 0.5*(targets[k]-self.ao[k])**2
        
        return error
    
    # accuracy evaluation on test dataset
    def test(self, act_func, patterns):
        count = 0
        for p in patterns:
            target = flowerLables[(p[1].index(1))]
            result = self.update(p[0], act_func)
            index = result.index(max(result))
            print(p[0], ':', target, '->', flowerLables[index])
            count += (target == flowerLables[index])
        accuracy = float(count/len(patterns))
        print('accuracy: %-.9f' % accuracy)
        
    # learned weights printing
    def weights(self):
        print('\nWeights for Input Layer:')
        for i in range(self.ni):
            print(self.wi[i])
            print ""

        print('\nWeights for Output Layer:')
        for j in range(self.nh):
            print(self.wo[j])
            print ""

    def train(self, act_func, patterns, iterations=1000, N=0.1, M=0.01):
        # N: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                # sample inputs = [6.3, 3.4, 5.6, 2.4]
                # sample targets = [0, 0, 1]
                inputs = p[0]
                targets = p[1]
                self.update(inputs, act_func)
                error = error + self.backPropagate(targets, act_func, N, M)
            if i % 100 == 0:
                print('Current Error: %-.9f' % error)

def main():
    
    # dataset information
    filename = "iris.data.txt"
    column = ['SepalLength','SepalWidth','PetalLength','PetalWidth', 'Class']
    
    data = []
    raw = pd.read_table(filename, names=column, sep=',')
    raw_data = raw.values
    raw_feature = raw_data[0:,0:4]
    
    # label added to raw data
    for i in range(len(raw_feature)):
        ele = []
        ele.append(list(raw_feature[i]))
        if raw_data[i][4] == 'Iris-setosa':
           ele.append([1,0,0])
        elif raw_data[i][4] == 'Iris-versicolor':
            ele.append([0,1,0])
        else:
            ele.append([0,0,1])
        data.append(ele)

    # randomize sequence of data
    random.shuffle(data)
    
    # seperate data to training and test set
    train = data[0:100]
    test = data[101:]
    
    # parameter setting for NN
    nn = NN(4,7,3)
    act_func = "tanh"
    nn.train(act_func, train, iterations=10000)
    
    # print the learned weights
    nn.weights()
    
    # model test
    nn.test(act_func, test)
    
main()

