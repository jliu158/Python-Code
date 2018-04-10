import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk



# load data
global dataarray
dataarray = np.loadtxt('points.dat.txt')
dataarray = np.mat(dataarray)


'''E Step'''
def e_step(alpha, mu, sigma):
    global dataarray
    global k
    global N
    #global mu
    #global sigma
    #global alpha
    global w
    w = np.zeros((N, k))
    for i in range(N):
        denom = 0
        # each sample of points
        for j in range(k):
            # each mixture
            #print np.mat(sigma[j]).I
            numor = alpha[j] * np.exp(-0.5*(dataarray[i] - mu[j]) * np.mat(sigma[j]).I * (dataarray[i] - mu[j]).T)/(2*np.pi * np.sqrt(np.linalg.det(np.mat(sigma[j]))))
            # calculate the numor
            denom += numor  # calculate the denom

        for j in range(k):
            numor = alpha[j] * np.exp(-0.5*(dataarray[i] - mu[j]) * np.mat(sigma[j]).I * (dataarray[i] - mu[j]).T)/(2*np.pi * np.sqrt(np.linalg.det(np.mat(sigma[j]))))
            # calculate the numor
            w[i,j] = numor/denom  # generate the matrix of each numor
    return w
    #print w



'''M Step'''
def m_step(w):
    global dataarray
    global alpha
    #global w
    global sigma
    global mu
    global N
    global tied
    global k
    #print sigma

    sigma_sum = 0
    for j in range(k):
        denom = 0  # sum of w
        numer = 0  # sum of w*x
        numer_sigma = 0 # numor for sigma
        for i in range(N):
            numer += w[i, j] * dataarray[i]
            denom += w[i, j]
            numer_sigma += w[i, j]*(dataarray[i] - mu[j]).T*(dataarray[i] - mu[j])
        mu[j, :] = numer / denom  # Mean
        alpha[j] = denom / N  # Mixture coefficient
        sigma[j] = numer_sigma/denom      # Covariance matrix\sigma
    #print sigma
    if tied:
        for j in range(k):
            sigma[j] = sigma_sum/k
        #print sigma
    return alpha, mu, sigma


#if __name__ == '__main__':

#global k
k = 2   # number of mixture
tied = False # tied or whether
#global N
dataarray = dataarray[:900]
N = dataarray.shape[0]  # number of points
# Initial all the parameters
alpha = []
mu = []
sigma = []
for j in range(k):
    alpha.append(1.0/k)   # Coefficient 1/k
    mean = sum(dataarray)/N  # calculate the mean of the points
    mu_ = mean + np.random.random((1,2))
    mu.append(mu_.tolist()[0])
    sigma.append(np.mat([[1, 0], [0, 1]]))

mu = np.mat(mu)     # mu matrix form
#print mu


#alpha = [0.5, 0.5]  # Mixture coefficient

#mu = np.random.random((2,2))
#print mu


#sigma=[[[1, 0], [0, 1]],[[1, 0], [0, 1]]]   # Covariance matrix


iteration = 10     # set the iteration times

def likelihood(alpha, mu, sigma):
    #global alpha
    global dataarray
    #global sigma
    #global mu
    global N
    global k
    llh = 0
    # calculate the likelihood
    for i in range(N):
        mix_llh = 0
        for j in range(k):
            mix_llh += np.log(alpha[j]*np.exp(-0.5 * (dataarray[i] - mu[j]) * np.mat(sigma[j]).I * (dataarray[i] - mu[j]).T) / (2 * np.pi * np.sqrt(np.linalg.det(np.mat(sigma[j])))))
            #print mix_llh[0,0]
        llh += mix_llh[0,0]
    llh = llh/N
    return llh

ans = []
for i in range(iteration):
    w = e_step(alpha, mu, sigma)
    alpha, mu, sigma = m_step(w)
    #print alpha
    ans.append(likelihood(alpha, mu, sigma))
    print ans

#plt.plot(ans)
#plt.show()

#print (dataarray[1]-mu[1])*sigma.I*(dataarray[1]-mu[1]).T
