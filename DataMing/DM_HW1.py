#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

raw_data = open('iris.data.txt')
line = raw_data.readline()
new_dataset = [[], [], [], []]
while line:
    if line == ' ':
        break
    line_data = line.strip('\n').split(',')
    for i in range(4):
        if line_data[i] == '':
            break
        new_dataset[i].append(float(line_data[i]))
    line = raw_data.readline()

#new_dataset = np.transpose(np.mat(new_dataset))

print new_dataset
setosa = [new_dataset[0][:50], new_dataset[1][:50], new_dataset[2][:50], new_dataset[3][:50]]
versicolor = [new_dataset[0][50:100], new_dataset[1][50:100], new_dataset[2][50:100], new_dataset[3][50:100]]
virginica = [new_dataset[0][100:], new_dataset[1][100:], new_dataset[2][100:], new_dataset[3][100:]]


#all_data = [np.random.normal(0, std, 100) for std in range(1, 4)]
#print type(all_data)

''' Boxplots for three kinds of iris '''
fig1 = plt.figure(figsize=(12, 6))

plt.subplot(1,3,1)
plt.boxplot(setosa)
plt.yticks([0,1,2,3,4,5,6,7,8])
plt.xticks([y + 1 for y in range(len(new_dataset))], ['sep_len', 'sep_wid', 'pet_len', 'pet_wid'])
plt.xlabel('Attribute Information in cm')
t = plt.title('Iris-Setosa Boxplot')

plt.subplot(1,3,2)
plt.boxplot(versicolor)
plt.yticks([0,1,2,3,4,5,6,7,8])
plt.xticks([y + 1 for y in range(len(new_dataset))], ['sep_len', 'sep_wid', 'pet_len', 'pet_wid'])
plt.xlabel('Attribute Information in cm')
t = plt.title('Iris-Versicolor Boxplot')

plt.subplot(1,3,3)
plt.boxplot(virginica)
plt.yticks([0,1,2,3,4,5,6,7,8])
plt.xticks([y + 1 for y in range(len(new_dataset))], ['sep_len', 'sep_wid', 'pet_len', 'pet_wid'])
plt.xlabel('Attribute Information in cm')
t = plt.title('Iris-Virginica Boxplot')


''' Histogram for three kinds of iris '''
fig2 = plt.figure(figsize=(14, 6))

plt.subplot(1,4,1)
plt.hist(setosa[0], alpha=0.5, label='Setosa', color='red')
plt.hist(versicolor[0], alpha=0.5, label='Versicolor', color='blue')
plt.hist(virginica[0], alpha=0.5, label='Virginica', color='green')
t = plt.title('Iris Sepal length')

plt.subplot(1,4,2)
plt.hist(setosa[1], alpha=0.5, label='Setosa', color='red')
plt.hist(versicolor[1], alpha=0.5, label='Versicolor', color='blue')
plt.hist(virginica[1], alpha=0.5, label='Virginica', color='green')
t = plt.title('Iris Sepal width')

plt.subplot(1,4,3)
plt.hist(setosa[2], alpha=0.5, label='Setosa', color='red')
plt.hist(versicolor[2], alpha=0.5, label='Versicolor', color='blue')
plt.hist(virginica[2], alpha=0.5, label='Virginica', color='green')
t = plt.title('Iris Petal length')

plt.subplot(1,4,4)
plt.hist(setosa[3], alpha=0.5, label='Setosa', color='red')
plt.hist(versicolor[3], alpha=0.5, label='Versicolor', color='blue')
plt.hist(virginica[3], alpha=0.5, label='Virginica', color='green')
plt.legend(loc='upper right')
t = plt.title('Iris Petal Width')


''' Scatter plot for three kinds of iris '''
fig3 = plt.figure(figsize=(12,6))

plt.subplot(1,2,1)
plt.scatter(setosa[0], setosa[1], marker='o', color='r', label='Setosa')
plt.scatter(versicolor[0], versicolor[1], marker='o', color='b', label='Versicolor')
plt.scatter(virginica[0], virginica[1], marker='o', color='g', label='Virginica')
plt.ylabel('sepal width')
plt.xlabel('sepal length')
plt.title('Iris Sepal Size')
plt.legend(loc='upper right')

plt.subplot(1,2,2)
plt.scatter(setosa[2], setosa[3], marker='o', color='r', label='Setosa')
plt.scatter(versicolor[2], versicolor[3], marker='o', color='b', label='Versicolor')
plt.scatter(virginica[2], virginica[3], marker='o', color='g', label='Virginica')
plt.ylabel('petal width')
plt.xlabel('petal length')
plt.title('Iris Petal Size')
plt.legend(loc='upper right')


plt.show()