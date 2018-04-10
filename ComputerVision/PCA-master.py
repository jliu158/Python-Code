import numpy as np
from sklearn.decomposition import PCA
import h5py

f = h5py.File('train_fc7.h5','r')
print(f['fc7_features'].shape)


X = np.array([[-1, -1, 1], [-2, -1, 2], [-3, -2, 3], [1, 1, 4], [2, 1,-1], [3, 2, 1]])
y = np.array([1, 2, 3, 4, 5, 6])
pca = PCA(n_components=256)

print(pca.fit_transform(f['fc7_features'][0]).shape)