from modis_dataset_gen import modis_dataset_generator
from modis_cld_msk import cloud_mask_generator
import os
import numpy as np
from scipy import misc

MOD021KM_data_path = '/projects/TDataFus/gyzhao/TF/data/MODIS/MOD021KM'
MOD03_data_path = '/projects/TDataFus/gyzhao/TF/data/MODIS/MOD03'
MOD06_L2_data_path = '/projects/TDataFus/gyzhao/TF/data/MODIS/MOD06_L2'

def npz_image_generator(year=2010, month=None,npz=False,img=True):
    if npz == True:
        print 'Generating npz from year', year
    if img == True:
        print 'Generating img from year', year
    MOD021KM_path = MOD021KM_data_path + '/' + str(year)
    MOD03_path = MOD03_data_path + '/' + str(year)
    MOD06_L2_path = MOD06_L2_data_path + '/' + str(year)

    MOD021_days = os.listdir(MOD021KM_path)
    MOD03_days = os.listdir(MOD03_path)
    MOD06_L2_days = os.listdir(MOD06_L2_path)

    total_days = len(MOD021_days)
    count = 0
    temp_sample_name = 'sample.jpg'
    temp_mask_name = 'mask.jpg'
    for i in range(total_days):
        MOD021_cur_directory = MOD021KM_path + '/' + MOD021_days[i]
        MOD03_cur_directory = MOD03_path + '/' + MOD03_days[i]
        MOD06_L2_cur_directory = MOD06_L2_path + '/' + MOD06_L2_days[i]
        total_files_within_single_day = os.listdir(MOD021_cur_directory)
        for j in range(len(total_files_within_single_day)):
            cur_MOD021 = MOD021_cur_directory + '/' + os.listdir(MOD021_cur_directory)[j]
            cur_MOD03 = MOD03_cur_directory + '/' + os.listdir(MOD03_cur_directory)[j]
            cur_MOD06_L2 = MOD06_L2_cur_directory + '/' + os.listdir(MOD06_L2_cur_directory)[j]
            modis_dataset_generator(cur_MOD021, temp_sample_name[0:6] + str(count) + temp_sample_name[-4:], cur_MOD03, npz=False, img=True)
            cur_img = misc.imread(temp_sample_name[0:6] + str(count) + temp_sample_name[-4:])
            #This is the case when image is blank; thus this sample and mask will be disgarded
            if np.any(cur_img) == False:
                os.remove(temp_sample_name[0:6] + str(count) + temp_sample_name[-4:])
                break
            cloud_mask_generator(cur_MOD06_L2, temp_mask_name[0:4] + str(count) + temp_sample_name[-4:], True, npz=False, img=True)
            count += 1

'''
modis_dataset_generator("MOD021KM.A2010001.1300.006.2014223214136.hdf","output1.npz","MOD03.A2004026.1230.006.2012274025923.hdf")
curr_data = np.load("sample10.npz")
curr_image = curr_data["arr_0"]

labels_file = cloud_mask_generator("MOD06_L2.A2004026.1230.006.2014332063358.hdf","label_output.npz",True)
labels_dict = np.load("mask10.npz")
image_labels = labels_dict["cloud_mask"]

source = '/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system'
dest1 = '/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system/train_img'
dest2 = '/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system/train_mask'

files = os.listdir(source)

for f in files:
    if (f.startswith("sample")):
        shutil.move(f, dest1)
    elif (f.startswith("mask")):
        shutil.move(f, dest2)

modis_dataset_generator("MOD021KM.A2010001.1300.006.2014223214136.hdf","test_img.jpg","MOD03.A2010001.1300.006.2012280165209.hdf",npz=False,img=True)
labels_file = cloud_mask_generator("MOD06_L2.A2010001.1300.006.2015041191320.hdf","test_mask.jpg",True,npz=False,img=True)
'''
npz_image_generator()