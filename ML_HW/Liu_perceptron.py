#!/usr/bin/python
import argparse
import numpy as np


def Create_Dataset(datatype):
    raw_data = open('/u/cs246/data/adult/a7a.' + datatype)
    line = raw_data.readline()
    new_dataset = []
    new_class = []
    while line:
        new_record = [0.0]*123 + [1.0]
        line_data = line.split(' ')
        new_class.append(int(line_data[0]))
        for info in line_data[1:-1]:
            info_index = info.split(':')
            new_record[int(info_index[0])] = 1.0
        line = raw_data.readline()
        new_dataset.append(new_record)
    return np.array(new_dataset), new_class







# sign function
def Sign(result):
    if result < 0:
        return -1
    elif result == 0:
        return 0
    elif result > 0:
        return 1

# Main function for perceptron
def Perceptron(train_set, train_class, dev_set, dev_class, noDev = False, iterations = 5):
    weight = np.mat([0.0]*124)
    #global train_set, train_class, dev_set, dev_class
    prev_accu = 0
    if noDev == True:   # without dev set
        for iter in range(iterations):
            # run for iterations times
            for i in range(len(train_set)):
                # run for each instance
                y_i = Sign(np.sum(np.multiply(weight, train_set[i])))
                y = train_class[i]  # the correct y value for instance
                if y_i != train_class[i]:
                    weight += float(y) * train_set[i] * 1  # update the weight by adding xy, lr is 1
            #print weight
    else:
        while True: # with dev set
            # run for iterations times
            for i in range(len(train_set)):
                # run for each instance
                y_i = Sign(np.sum(np.multiply(weight, train_set[i])))
                y = train_class[i]  # the correct y value for instance
                #print (train_set[i])
                #print train_set[i] * lr * float(y)
                if y_i != train_class[i]:
                    weight += float(y) * train_set[i] * 1  # update the weight by xy, lr is 1
            # use dev to validate the best learning rate and iterations
            accu = Test(weight, dev_set, dev_class)
            # check the accuracy on dev set, if the difference is smaller than 0.02, then stop
            if abs(accu - prev_accu) < 0.0001:
                break
            prev_accu = accu
    return weight


# Test the accuracy
def Test(weight, test_set, test_class):
    cor_num = 0 # stand for the number of correct instances
    for i in range(len(test_class)):
        y_i = Sign(np.sum(np.multiply(weight, test_set[i])))
        y = test_class[i]
        if y_i == y:
            cor_num += 1
    return cor_num/float(len(test_class))



# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parameters to control the perceptron')

    parser.add_argument('--nodev', action="store_true", dest="nodev", default=False)
    parser.add_argument('--iterations', action="store", dest="iteration_number", type=int)

    noDev = parser.parse_args().nodev  # get the nodev parameter from cmd
    iterations = parser.parse_args().iteration_number  # get the iteration number from cmd


    # create the datasets from given files
    test_set, test_class = Create_Dataset('test')
    train_set, train_class = Create_Dataset('train')
    dev_set, dev_class = Create_Dataset('dev')

    # use Perceptron function to calculate the weight and test the final accuracy
    weight = Perceptron(train_set, train_class, dev_set, dev_class, noDev, iterations)
    print("Test accuracy: %s" % Test(weight, test_set, test_class))
    print("Feature weights (bias last): %s" % weight)


'''
weight = Perceptron()
print weight
print Test(weight, test_set, test_class)

'''