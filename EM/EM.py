import numpy as np
import matplotlib.pyplot as plt#!/usr/bin/python
import argparse
np.random.seed(2)


def EM(num_mixture, tied, x):
    num_samples=len(x)
    num_iteration=100
    likelihood_train=[0]*num_iteration
    likelihood_dev=[0]*num_iteration

    w=0.01*np.random.random((num_samples,num_mixture))

    #print type(x)
    x_train=x[0:900]
    for n in xrange(num_iteration):

        # M Step
        sigma=np.zeros((num_mixture,2,2))
        phi=np.sum(w[0:900],axis=0)/num_samples
        mu=np.matmul(w[0:900].T,x_train)
        w_sum=np.sum(w[0:900],axis=0)

        for i in xrange(num_mixture):
            mu[i,:]=mu[i,:]/w_sum[i]


        for i in xrange(num_mixture):
            for j in xrange(900):
                sigma[i,:,:]+=w[j,i]*np.matmul(np.reshape((x[j]-mu[i]),(2,1)),np.reshape((x[j]-mu[i]),(1,2)))
            sigma[i,:,:]=sigma[i,:,:]/w_sum[i]

        if tied == True:

            for i in xrange(num_mixture):
                sigma[i, :, :]=phi[i]*sigma[i,:,:]

            sigma_mean = np.sum(sigma, axis=0,keepdims=True)
            for i in xrange(num_mixture):
                sigma[i, :, :] = sigma_mean

        # E Step
        for i in xrange(1000):
            alpha=0
            L_train = 0
            L_dev = 0
            if i<900:
                for j in xrange(num_mixture):
                    exp=-0.5*np.matmul(np.reshape((x[i]-mu[j]),(1,2)),np.linalg.inv(sigma[j,:,:]))
                    exp=np.matmul(exp,np.reshape((x[i]-mu[j]),(2,1)))
                    w[i,j]=(1/(2*np.pi))*(1/np.linalg.det(sigma[j]))**0.5*np.exp(exp)  *phi[j]
                    L_train+=w[i,j]
                    alpha+=w[i,j]

                likelihood_train[n]+=np.log(L_train)/900
                w[i,:]=w[i,:]/alpha
            else:
                for j in xrange(num_mixture):
                    exp = -0.5 * np.matmul(np.reshape((x[i] - mu[j]), (1, 2)), np.linalg.inv(sigma[j, :, :]))
                    exp = np.matmul(exp, np.reshape((x[i] - mu[j]), (2, 1)))
                    w[i, j] = (1 / (2 * np.pi)) * (1 / np.linalg.det(sigma[j])) ** 0.5 * np.exp(exp) * phi[j]
                    L_dev += w[i, j]
                likelihood_dev[n] += np.log(L_dev)/100


    plt.plot(likelihood_train[1:])
    plt.plot(likelihood_dev[1:])
    if tied:
        mode = 'Tied'
    else:
        mode = 'Seperated'
    title=mode+' '+'Mixture:'+str(num_mixture)
    plt.title(title)
    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parameters to control the perceptron')

    parser.add_argument('--k', action="store", dest="k", type=int)
    parser.add_argument('--tied', action="store_true", dest="tied", default=False)

    k = parser.parse_args().k  # get the number of mixture from cmd
    tied = parser.parse_args().tied  # get the mode:tied or seperated from cmd
    # load data
    data = np.loadtxt('points.dat')
    data = np.array(data)
    # tied or seperate

    EM(k,tied,data)


