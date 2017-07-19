import os
import numpy as np
import sklearn
from sklearn.naive_bayes import GaussianNB
from modis_dataset_gen import modis_dataset_generator
from modis_cld_msk import cloud_mask_generator
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.svm import SVC

def gaussian_naive_bayes(training_data,training_labels):
    clf = GaussianNB()
    clf.fit(training_data,training_labels)
    y_pred = clf.predict(training_data)
    print(accuracy_score(training_labels,y_pred)*100)
    return
def pca_data(training_data,no_components=2):
    pca = PCA(n_components=no_components)
    return pca.fit_transform(training_data)

def SVM(training_data,training_labels,pca=False):
    clf = SVC()
    if(pca==True):
        training_data = pca_data(training_data)
    clf.fit(training_data,training_labels)
    y_pred = clf.predict(training_data)
    print(accuracy_score(training_labels,y_pred)*100)
    return

#arr = #assume the array is obtained
modis_dataset_generator("MOD021KM.A2004026.1230.006.2014218105922.hdf","output1.npz","MOD03.A2004026.1230.006.2012274025923.hdf")
curr_data = np.load("output1.npz")

curr_image = curr_data["arr_0"]

labels_file = cloud_mask_generator("MOD06_L2.A2004026.1230.006.2014332063358.hdf","label_output.npz",True)
labels_dict = np.load("label_output.npz")
image_labels = labels_dict["cloud_mask"]

#gaussian_naive_bayes(curr_image,image_labels)
#SVM(curr_image,image_labels)
#SVM(curr_image,image_labels,True)

#no_components = 2

#print(curr_image.shape)







#def main():
