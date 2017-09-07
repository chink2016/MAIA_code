import os,sys
from os import listdir
from os.path import isfile, join
import sys, os
script_dir = sys.path[0]
img_path = os.path.join(script_dir, '../train_img')

sys.path.append('/Users/ningkaiwu/tf-image-segmentation')
sys.path.append('/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system/train_img')
sys.path.append('/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system/train_mask')

os.environ["CUDA_VISIBLE_DEVICES"] = '1'

from tf_image_segmentation.utils.tf_records import write_image_annotation_pairs_to_tfrecord

train_img_path = 'train_img'
train_mask_path = 'train_mask'
list_a = [f for f in listdir(train_img_path) if isfile(join(train_img_path, f))]
#print(list_a)
#print(len(list_a))
list_b = [f for f in listdir(train_mask_path) if isfile(join(train_mask_path, f))]
print(list_b)
print(len(list_b))
file_names = zip(list_a, list_b)
print(file_names)
print(len(file_names))
files_names = []
for pair in file_names:
    image_path = '/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system/train_img/' + pair[0]
    mask_path = '/Users/ningkaiwu/PycharmProjects/MAIA_code-master/MAIA_system/train_mask/' + pair[1]
    cur_pair = (image_path,mask_path)
    files_names.append(cur_pair)
print(files_names)
# You can create your own tfrecords file by providing
# your list with (image, annotation) filename pairs here

write_image_annotation_pairs_to_tfrecord(filename_pairs=files_names,
                                         tfrecords_filename='cloud_augmented_train.tfrecords')