#!/usr/bin/python
import argparse
import numpy as np


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
def SVM(train_set, train_class, dev_set, dev_class, iterations = 1, capacity = 0.868):
    N = len(train_set)
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
    #train_accu = Test(weight, bias, train_set, train_class)
    #print train_accu

    # check the accuracy on dev set
    #dev_accu = Test(weight, bias, dev_set, dev_class)
    #print dev_accu



    return weight, bias


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
#test_set, test_class = Create_Dataset('test')
#train_set, train_class = Create_Dataset('train')
#dev_set, dev_class = Create_Dataset('dev')




# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parameters to control the perceptron')

    #parser.add_argument('--nodev', action="store_true", dest="nodev", default=False)
    parser.add_argument('--epochs', action="store", dest="iteration_number", type=int)
    parser.add_argument('--capacity', action='store', dest='parameter_C', type=float)

    #noDev = parser.parse_args().nodev  # get the nodev parameter from cmd
    epochs = parser.parse_args().iteration_number  # get the iteration number from cmd
    capacity = parser.parse_args().parameter_C  # get the hyper-parameter C


    # create the datasets from given files
    test_set, test_class = Create_Dataset('test')
    train_set, train_class = Create_Dataset('train')
    dev_set, dev_class = Create_Dataset('dev')

    # use Perceptron function to calculate the weight and test the final accuracy
    weight, bias = SVM(train_set, train_class, dev_set, dev_class, epochs, capacity)
    print("EPOCHS: %s" % epochs)
    print("CAPACITY: %s" % capacity)
    print("TRAINING_ACCURACY: %s" % Test(weight, bias, train_set, train_class))
    print("TEST_ACCURACY: %s" % Test(weight, bias, test_set, test_class))
    print("DEV_ACCURACY: %s" % Test(weight, bias, dev_set, dev_class))
    print("FINAL_SVM: %s" % ([bias] + weight.tolist()[0]))
