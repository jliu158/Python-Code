import math
import matplotlib.pyplot as plt

age = [23, 23, 27, 27, 39, 41, 47, 49, 50, 52, 54, 54, 56, 57, 58, 58, 60, 61]

percent_fat = [9.5, 26.5, 7.8, 17.8, 31.4, 25.9, 27.4, 27.2, 31.2, 34.6, 42.5, 28.8, 33.4, 30.2, 34.1, 32.9, 41.2, 35.7]

age_sort = sorted(age)

print sum(age)/float(len(age))

def std(l):
    mean = sum(l)/float(len(l))
    pow_sum = 0
    for num in l:
        pow_sum += pow(num-mean, 2)
    return math.sqrt(pow_sum/float(len(l)))


print std(age)


print (age_sort[8]+age_sort[9])/float(2)

print sum(percent_fat)/18.0

print std(percent_fat)
fat_sort = sorted(percent_fat)
print (fat_sort[8]+fat_sort[9])/2.0

import numpy as np
from scipy.stats import percentileofscore
#ref = np.asarray(age)
#print ref
samp_age = np.asarray([percentileofscore(age, x) for x in age])
samp_fat = np.asarray([percentileofscore(percent_fat, x) for x in percent_fat])
print samp_age
print samp_fat

print math.pow(pow(2,4) + pow(6,4)+1+pow(2,4), 0.25)
'''
#plt.boxplot(percent_fat)
plt.scatter(samp_age, samp_fat, marker='o', color='r')
plt.plot([0,120], [0,120])
plt.xlim([0,120])
plt.ylim([0,120])
plt.title('Quantile-Quantile Plot')
plt.xlabel('Age Quantiles')
plt.ylabel('%Fat Quantiles')
plt.show()
'''


age = [13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70]
print len(age)
plt.hist(age, bins=np.arange(0, 100, 10))
#plt.show()

def modelPoint(a,b):
    _a = a * math.sqrt(1/(pow(a,2) + pow(b,2)))
    _b = b * math.sqrt(1/(pow(a,2) + pow(b,2)))
    d = math.sqrt(pow(_a - 1.4, 2) + pow(_b - 1.6, 2))
    return _a, _b, d


print modelPoint(1.5, 1.7)
print modelPoint(2, 1.9)
print modelPoint(1.6, 1.8)
print modelPoint(1.2, 1.5)
print modelPoint(1.5, 1.0)