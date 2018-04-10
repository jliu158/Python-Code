# -*- coding: utf-8 -*-

from numpy import *
import numpy as np
import pandas as pd
from math import log
import operator


# 计算数据集的香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    # 给所有可能分类创建字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    # 以2为底数计算香农熵
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


# 对离散变量划分数据集，取出该特征取值为value的所有样本
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


# 对连续变量划分数据集，direction规定划分的方向，
# 决定是划分出小于value的数据样本还是大于value的数据样本集
def splitContinuousDataSet(dataSet, axis, value, direction):
    retDataSet = []
    for featVec in dataSet:
        if direction == 0:
            if featVec[axis] > value:
                reducedFeatVec = featVec[:axis]
                reducedFeatVec.extend(featVec[axis + 1:])
                retDataSet.append(reducedFeatVec)
        else:
            if featVec[axis] <= value:
                reducedFeatVec = featVec[:axis]
                reducedFeatVec.extend(featVec[axis + 1:])
                retDataSet.append(reducedFeatVec)
    return retDataSet


# 选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet, labels):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    bestSplitDict = {}
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        # 对连续型特征进行处理
        if type(featList[0]).__name__ == 'float' or type(featList[0]).__name__ == 'int':
            # 产生n-1个候选划分点
            sortfeatList = sorted(featList)
            splitList = []
            for j in range(len(sortfeatList) - 1):
                splitList.append((sortfeatList[j] + sortfeatList[j + 1]) / 2.0)

            bestSplitEntropy = 10000
            slen = len(splitList)
            # 求用第j个候选划分点划分时，得到的信息熵，并记录最佳划分点
            for j in range(slen):
                value = splitList[j]
                newEntropy = 0.0
                subDataSet0 = splitContinuousDataSet(dataSet, i, value, 0)
                subDataSet1 = splitContinuousDataSet(dataSet, i, value, 1)
                prob0 = len(subDataSet0) / float(len(dataSet))
                newEntropy += prob0 * calcShannonEnt(subDataSet0)
                prob1 = len(subDataSet1) / float(len(dataSet))
                newEntropy += prob1 * calcShannonEnt(subDataSet1)
                if newEntropy < bestSplitEntropy:
                    bestSplitEntropy = newEntropy
                    bestSplit = j
            # 用字典记录当前特征的最佳划分点
            bestSplitDict[labels[i]] = splitList[bestSplit]
            infoGain = baseEntropy - bestSplitEntropy
        # 对离散型特征进行处理
        else:
            uniqueVals = set(featList)
            newEntropy = 0.0
            # 计算该特征下每种划分的信息熵
            for value in uniqueVals:
                subDataSet = splitDataSet(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                newEntropy += prob * calcShannonEnt(subDataSet)
            infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    # 若当前节点的最佳划分特征为连续特征，则将其以之前记录的划分点为界进行二值化处理
    # 即是否小于等于bestSplitValue
    if type(dataSet[0][bestFeature]).__name__ == 'float' or type(dataSet[0][bestFeature]).__name__ == 'int':
        bestSplitValue = bestSplitDict[labels[bestFeature]]
        labels[bestFeature] = labels[bestFeature] + '<=' + str(bestSplitValue)
        for i in range(shape(dataSet)[0]):
            if dataSet[i][bestFeature] <= bestSplitValue:
                dataSet[i][bestFeature] = 1
            else:
                dataSet[i][bestFeature] = 0
    return bestFeature


# 特征若已经划分完，节点下的样本还没有统一取值，则需要进行投票
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    return max(classCount)


# 主程序，递归产生决策树
def createTree(dataSet, labels, data_full, labels_full):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet, labels)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    if type(dataSet[0][bestFeat]).__name__ == 'str':
        currentlabel = labels_full.index(labels[bestFeat])
        featValuesFull = [example[currentlabel] for example in data_full]
        uniqueValsFull = set(featValuesFull)
    del (labels[bestFeat])
    # 针对bestFeat的每个取值，划分出一个子树。
    for value in uniqueVals:
        subLabels = labels[:]
        if type(dataSet[0][bestFeat]).__name__ == 'str':
            uniqueValsFull.remove(value)
        myTree[bestFeatLabel][value] = createTree(splitDataSet \
                                                      (dataSet, bestFeat, value), subLabels, data_full, labels_full)
    if type(dataSet[0][bestFeat]).__name__ == 'str':
        for value in uniqueValsFull:
            myTree[bestFeatLabel][value] = majorityCnt(classList)
    return myTree



''' 画出决策树 '''
#import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


# 计算树的叶子节点数量
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


# 计算树的最大深度
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth


# 画节点
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', \
                            xytext=centerPt, textcoords='axes fraction', va="center", ha="center", \
                            bbox=nodeType, arrowprops=arrow_args)


# 画箭头上的文字
def plotMidText(cntrPt, parentPt, txtString):
    lens = len(txtString)
    xMid = (parentPt[0] + cntrPt[0]) / 2.0 - lens * 0.002
    yMid = (parentPt[1] + cntrPt[1]) / 2.0
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]
    cntrPt = (plotTree.x0ff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.y0ff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.y0ff = plotTree.y0ff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.x0ff = plotTree.x0ff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.x0ff, plotTree.y0ff), cntrPt, leafNode)
            plotMidText((plotTree.x0ff, plotTree.y0ff), cntrPt, str(key))
    plotTree.y0ff = plotTree.y0ff + 1.0 / plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.x0ff = -0.5 / plotTree.totalW
    plotTree.y0ff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


'''10-folds Cross Validation'''
def get_index(node, standard_v):
    for i in range(len(standard_v)):
        if standard_v[i] == node:
            return i



# {'Patrons': {'None': 'No', 'Full': {'Hungry': {'Yes': {'Type': {'Burger': 'Yes', 'Thai': {'Fri/Sat': {'Yes': 'Yes', 'No': 'No'}}, 'French': 'Yes', 'Italian': 'No'}}, 'No': 'No'}}, 'Some': 'Yes'}}
def validation_data(tree, vector, standard_v):
    global index
    if type(tree) != dict:
        if tree == vector[-1]:
            index += 1
            return
        else:
            return
    attr_index = get_index(tree.keys()[0], standard_v)
    for value in tree.values()[0]:
        if value == vector[attr_index]:
            validation_data(tree.values()[0][value], vector, standard_v)

# ten_fold
def ten_fold(dataset, labels):
    global index
    lenth = len(dataset)
    one_batch = lenth//10
    accuracy = 0
    for i in range(10):
        index = 0
        dataset_split = dataset[:]
        test_set = dataset_split[i*one_batch: (i+1)*one_batch]
        train_set = dataset_split[:i*one_batch] + dataset_split[(i+1)*one_batch:]
        test_dataset(train_set[:], test_set[:], labels[:])
        accuracy += index/float(len(test_set))
    return (accuracy/float(10))


# test the splited training dataset and test dataset
def test_dataset(train_set, test_set, labels):
    standard_v = labels[:]
    myTree = createTree(train_set, labels, train_set[:], labels[:])
    for test_data in test_set:
        validation_data(myTree, test_data, standard_v)












# test the WillWait data set
def test_WillWait_tenfold():
    # get the data set
    data = []
    with open('WillWait-data.txt') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            line = line.split(',')
            data.append(line)
            line = f.readline()

    # get the decision tree labels
    label = []
    with open('WillWait-desc.txt') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            line = line[:-1]
            line = line.split(':')
            label.append(line[0])
            line = f.readline()
    labels = label[2:]

    # ten-fold validation
    #return ten_fold(data, labels)

    myTree = createTree(data, labels, data[:], labels[:])
    print(myTree)

    #validation_data(myTree, ['Yes', 'No', 'No', 'Yes', 'Full', '$', 'No', 'No', 'Thai', '30-60', 'No'], ['Alternate', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons', 'Price', 'Rainng', 'Reservation', 'Type', 'WaitEstimate', 'WillWait'])
    #print(index)

    createPlot(myTree)


# test iris data set
def test_Iris_tenfold():
    # get the data set
    data = []
    with open('iris.data.discrete.txt') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            line = line.split(',')
            data.append(line)
            line = f.readline()
    data_full = data[:]

    # get the decision tree labels
    labels = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']

    return ten_fold(data, labels)
    labels_full = labels[:]
    myTree = createTree(data, labels, data_full, labels_full)
    createPlot(myTree)


def test_WillWait():
    # get the data set
    data = []
    with open('WillWait-data.txt') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            line = line.split(',')
            data.append(line)
            line = f.readline()
    data_test = data[:]
    # get the decision tree labels
    label = []
    with open('WillWait-desc.txt') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            line = line[:-1]
            line = line.split(':')
            label.append(line[0])
            line = f.readline()
    labels = label[2:]
    labels_test = labels[:]

    myTree = createTree(data, labels, data[:], labels[:])
    global index
    for v in data_test:
        validation_data(myTree, v, labels_test)

    print 'The accuracy for WillWait is: ', index/float(len(data_test))
    print myTree

    #createPlot(myTree)


def test_Iris():
    # get the data set
    data = []
    with open('iris.data.discrete.txt') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            line = line.split(',')
            data.append(line)
            line = f.readline()
    data_full = data[:]
    data_test = data[:]

    # get the decision tree labels
    labels = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
    labels_test = labels[:]

    #return ten_fold(data, labels)
    labels_full = labels[:]
    myTree = createTree(data, labels, data_full, labels_full)
    global index

    for v in data_test:
        validation_data(myTree, v, labels_test)
    print 'The accuracy for Iris is: ', index/float(len(data_test))
    print myTree
    #createPlot(myTree)


index = 0
#test_WillWait()
#test_Iris()

import sys
if __name__ == '__main__':
    test_WillWait()
    test_Iris()