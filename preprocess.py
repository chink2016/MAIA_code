import os
import numpy as np
import sklearn
from sklearn.decompostion import PCA
arr = #assume the array is obtained
no_components = 2

def perform_pca(training_data):

    pca = PCA(n_components=no_components)
    pca.fit(training_data)
    pca.transform(training_data)

    return training_data
