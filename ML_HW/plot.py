#!/usr/bin/python
import argparse
import numpy as np
import matplotlib.pyplot as plt


def Create_Dataset(datatype):
    raw_data = open('adult/a7a.' + datatype)
    line = raw_data.readline()
    new_dataset = []
    new_class = []
    while line:
        new_record = [0.0]*123
        line_data = line.split(' ')
        new_class.append(int(line_data[0]))
        for info in line_data[1:-1]:
            info_index = info.split(':')
            new_record[int(info_index[0])-1] = 1.0
        line = raw_data.readline()
        new_dataset.append(new_record)
    return np.array(new_dataset), new_class




# Main function for SVM
def SVM(train_set, train_class, dev_set, dev_class, test_set, test_class, iterations = 5):
    N = len(train_set)
    c_list = np.logspace(-3, 4, 20)
    test_list = []
    dev_list = []
    for capacity in c_list:
        #global train_set, train_class, dev_set, dev_class
        weight = np.mat([0.0]*123)
        bias = 0.0    # set the initial bias value
        for iter in range(iterations):
            # run for iterations times
            for i in range(len(train_set)):
                # run for each instance
                if (np.sum(np.multiply(weight, train_set[i])) + bias) * train_class[i] < 1:
                    weight -= (weight/N - capacity * train_class[i] * train_set[i]) * 0.1    # suppose the learning rate is 0.1
                    bias -= (-capacity * train_class[i]) * 0.1
                else:
                    # otherwise
                    weight -= (weight/N) * 0.1    # lr is 0.1

        # check the accuracy on test set
        test_accu = Test(weight, bias, test_set, test_class)
        test_list.append(test_accu)

        # check the accuracy on dev set
        dev_accu = Test(weight, bias, dev_set, dev_class)
        dev_list.append(dev_accu)


    return c_list, test_list, dev_list


# sign function
def Sign(result):
    if result < 0:
        return -1
    elif result == 0:
        return 0
    elif result > 0:
        return 1

# Test the accuracy
def Test(weight, bias, test_set, test_class):
    cor_num = 0 # stand for the number of correct instances
    for i in range(len(test_class)):
        y_i = Sign((np.sum(np.multiply(weight, test_set[i])) + bias))
        y = test_class[i]
        if y_i == y:
            cor_num += 1
    return cor_num/float(len(test_class))




# create the datasets from given files
test_set, test_class = Create_Dataset('test')
train_set, train_class = Create_Dataset('train')
dev_set, dev_class = Create_Dataset('dev')

c, test_list, dev_list = SVM(train_set, train_class, dev_set, dev_class, test_set, test_class)
result_list = []
for i in range(len(c)):
    result = []
    result.append(c[i])
    result.append(test_list[i])
    result.append(dev_list[i])
    result_list.append(result)
print result_list



plt.figure(figsize=(10,5))
plt.title('Plot of Capacity Performance')
plt.plot(c, test_list, '-', label='Test Accuracy')
plt.plot(c, dev_list, '-', label='Dev Accuracy')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.show()