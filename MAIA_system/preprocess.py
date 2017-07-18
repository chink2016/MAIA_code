import os
import numpy as np
import sklearn
from sklearn.naive_bayes import GaussianNB
from modis_dataset_gen import modis_dataset_generator
#arr = #assume the array is obtained
modis_dataset_generator("MOD021KM.A2004026.1230.006.2014218105922.hdf","output1.npz","MOD03.A2004026.1230.006.2012274025923.hdf")
curr_data = np.load("output1.npz")

curr_image = curr_data["arr_0"]

#no_components = 2

print(curr_image.shape)
