import numpy as np
#import matplotlib.pyplot as plt
import argparse
import sys
#parser = argparse.ArgumentParser()
#args = parser.parse_args()
def data_preprocess():
    global sample_num
    global dim
    global dataset,mode
    #print dataset
    i = 0
    if dataset == 'earthquake_clean':

        sample_num = 64
        dim = 2
        x = np.zeros((sample_num, dim + 1))
        for line in open("earthquake-clean.data.txt"):
            x[i] = line.split(',')
            i += 1

    if dataset == 'earthquake_noisy':

        sample_num = 72
        dim = 2
        x = np.zeros((sample_num, dim + 1))
        for line in open("earthquake-noisy.data.txt"):
            x[i] = line.split(',')
            i += 1

    if dataset == 'iris':

        sample_num = 100
        dim = 4
        x = np.zeros((sample_num, dim + 1))
        for line in open("iris.data.txt"):
            x[i, 0:dim] = line.split(',')[0:4]

            if line.split(',')[dim:dim + 1] == ['Iris-setosa\n']:
                x[i, dim:dim + 1] = 0
            if line.split(',')[dim:dim + 1] == ['Iris-versicolor\n']:
                x[i, dim:dim + 1] = 1

            i += 1

    y = x[:, dim:dim + 1]
    x = x[:, 0:dim]
    return x,y

def train(x,y,lr,epoch_num):

    global dim
    sample_num=np.shape(y)[0]
    w = 0.0001 * np.ones((dim + 1))
    for epoch in xrange(epoch_num):
        for idx in xrange(sample_num):

           label=y[idx,0]
           h=0
           x_item=np.concatenate((np.ones((1)),x[idx]))
           h=sum(x_item*w)
           if mode == 'perceptron':
            w = w + lr * (label - h) * x_item
           if mode=='logistic':
            if h<1 and h>0:
                w=w+lr*(label-h)*h*(1-h)*x_item
    return w

def test(x,y,w):
    sample_num=len(y)
    predicted = np.zeros((sample_num, 1))
    if dataset=='earthquake_noisy' or dataset=='earthquake_clean' :
        for idx in xrange(sample_num):
            if sum(np.concatenate(([1], x[idx])) * w) < 0.5:
                predicted[idx, 0] = 0
            else:
                predicted[idx, 0] = 1

    if dataset=='iris':
        for idx in xrange(sample_num):
            #print sum(np.concatenate(([1], x[idx])) * w)
            if sum(np.concatenate(([1],x[idx]))*w)<0.5:
                predicted[idx,0]=0
            elif sum(np.concatenate(([1], x[idx])) * w) < 1.5 \
                    and sum(np.concatenate(([1], x[idx])) * w) >=0.5 :
                predicted[idx, 0] = 1
            else:
                predicted[idx, 0] = 2

    correct=predicted-y
    correct=(np.sum(correct==0))
    accuracy=float(correct)/sample_num

    return accuracy


# ten_fold
def ten_fold(dataset, labels,lr,epoch_num):
    global index
    lenth = len(dataset)
    one_batch = lenth//10
    accuracy = 0
    for i in range(10):
        index = 0

        dataset_split = dataset[:]
        test_set = dataset_split[i*one_batch: (i+1)*one_batch]
        #print dataset_split[(i+1)*one_batch:]
        train_set = np.concatenate((dataset_split[:i*one_batch] , dataset_split[(i+1)*one_batch:]))
        # label split
        label_split = labels[:]
        test_label_set = label_split[i*one_batch: (i+1)*one_batch]
        train_label_set = np.concatenate((label_split[:i*one_batch] , label_split[(i+1)*one_batch:]))
        model = train(train_set, train_label_set,lr,epoch_num)
        accuracy += test(test_set, test_label_set, model)
        #accuracy += test(train_set, train_label_set, model)
    return (accuracy/float(10))

'''
def plot():
    print 'plotting ...'
    # Plot
    global x,y,epoch_num,lr,mode,dataset
    colors = (1, 0, 0)
    area = np.pi * 3
    epoch_num = 80000
    w = train(x, y, lr, epoch_num)
    test(x, y, w)
    boundary = 0
    if dataset == 'earthquake_noisy':
        boundary = 39
    if dataset == 'earthquake_clean':
        boundary = 29

    plt.scatter(x[0:boundary, 0], x[0:boundary, 1], s=area, c=colors, alpha=0.5)
    plt.title(dataset)
    plt.xlabel('x')
    plt.ylabel('y')

    colors = (0, 1, 0)

    plt.scatter(x[boundary:, 0], x[boundary:, 1], s=area, c=colors, alpha=0.5)
    plt.title(dataset)
    plt.xlabel('x')
    plt.ylabel('y')

    line_x = [4.0, 7.0]
    line_y = [(float(line_x[0] * w[1] + w[0]) - 0.5) / -w[2], (float(line_x[1] * w[1] + w[0]) - 0.5) / -w[2]]

    plt.plot(line_x, line_y)
    if dataset == 'earthquake_noisy' or dataset == 'earthquake_clean':
        plt.show()

'''
# test the splited training dataset and test dataset




#parser.add_argument('--mode', default=None)
#parser.add_argument('--dataset', default=None)
def main(mode,dataset):
    global x,y
    index = 0
    lr = 0.0001
    epoch_num = 2000
    print 'training'


    mode=mode
    dataset=dataset

    x,y=data_preprocess()
    print '10-fold accuracy is:', ten_fold(x,y,lr,epoch_num)
    #plot()

if __name__ =='__main__':
    mode=sys.argv[1]
    dataset=str(sys.argv[2])
    main(mode,dataset)
