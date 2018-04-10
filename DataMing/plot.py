TPR = [0.2,
0.2,
0.4,
0.6,
0.6,
0.8,
0.8,
0.8,
0.8,
1]

FPR = [
0,
0.2,
0.2,
0.2,
0.4,
0.4,
0.6,
0.8,
1,
0]

import matplotlib.pyplot as plt

plt.plot(FPR, TPR)
plt.xlim([0,1])
plt.ylim([0,1])
plt.xlabel("False positive rate (FPR)")
plt.ylabel('True positive rate (TPR)')
plt.title("ROC curve")

plt.plot([0,1], [0,1])


plt.show()