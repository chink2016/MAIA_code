#!/usr/bin/env python

import os
import numpy as np
import sys
from pyhdf.SD import *
import argparse
from PIL import Image


def img_generator(cld_img, output_file_name, width, height, flag):
	img = Image.new(flag,(width,height))
	if flag == "L":
		cld_img[cld_img == 0] = max(0x03*86, 0xff)
		cld_img[cld_img == 1] = 0x02*86
		cld_img[cld_img == 2] = 0x01*86
		cld_img[cld_img == 3] = 0x00*86
		img.putdata(cld_img)

	else:
		cld_mask = [0xff]*len(cld_img)
		img.putdata(zip(cld_img,cld_mask,cld_mask))
		data = np.array(img)
		red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
		mask1 = (red == 0x0) & (green == 0xff) & (blue == 0xff)
		mask2 = (red == 0x1) & (green == 0xff) & (blue == 0xff)
		mask3 = (red == 0x2) & (green == 0xff) & (blue == 0xff)
		mask4 = (red == 0x3) & (green == 0xff) & (blue == 0xff)
		data[:,:,:3][mask1] = [0xff, 0xff, 0xff] #cloudy
		data[:,:,:3][mask2] = [0x00, 0x80, 0xff] #uncertain
		data[:,:,:3][mask3] = [0x00, 0xcc, 0x00] #probably clear
		data[:,:,:3][mask4] = [0xff, 0x80, 0x00] #clear
		img = Image.fromarray(data)

	img.save(output_file_name)
	img.show()
	
	return img

def npzgenerator(cld_img, output_file_name):
	np.savez(output_file_name,cloud_mask = cld_img)
	return cld_img

def cloud_mask_generator(input_file,output_file,crop=False,npz=True,img=False,clr=False):

	# Default width and height
	w = 2030
	h = 1354

	# Cropped width and height
	w_n = 400
	h_n = 400

	w_l = w/2 - 200
	w_r = w_l + 400

	h_l = h/2 - 200
	h_r = h_l + 400

	# parser = argparse.ArgumentParser(description='This will produce a cloud mask image in grayscale')
	# parser.add_argument('-i','--input',required=True,help='Input hdf file name')
	# parser.add_argument('-o','--output',required=True,help='Output npz file name')
	# parser.add_argument('-c','--crop',action='store_false',help='If you want it to be true size')
	# parser.add_argument('-npz','--npz',action='store_true',help='Generates npz file')
	# parser.add_argument('-img','--img',action='store_true',help='Generates image file')
	# parser.add_argument('-clr','--clr',action='store_true',help='Generates colored image file')
	# args = parser.parse_args()

	#Obtaining file name
	hdf_file_name = input_file
	output_file_name = output_file

	mod_ver = 0

	# Find out if MOD35 or MOD06 file
	if (hdf_file_name.find("MOD35") != -1): mod_ver = 1

	# Produce image in color or grayscale
	if clr == True: color = "RGB" 
	else: color = "L"

	hdf = SD(hdf_file_name)

	cld_mask_str = "Cloud_Mask"

	if mod_ver == 0: cld_mask_str += "_1km"


	cld_mask = hdf.select(cld_mask_str)

	if mod_ver == 1:
		if(crop == False):
			cld_ds_0 = cld_mask[0]
		else:
			cld_ds_0 = cld_mask[0][w_l:w_r,h_l:h_r]
			w = w_n
			h = h_n

	# MOD06 section
	else:
		if crop == False:
			cld_ds_0 = cld_mask[:,:,0]		
		else:
			cld_ds_0 = cld_mask[w_l:w_r,h_l:h_r,0]
			w = w_n
			h = h_n
			
	cld_img = cld_ds_0
	cld_img = (np.int_(cld_img) >> 1) & 0x03
	cld_img = cld_img.ravel().reshape(h,w,order='F').ravel()
	
	if npz is True:
		return npzgenerator(cld_img,output_file_name)
	if img is True:
		return img_generator(cld_img,output_file_name, w, h, color)

# if __name__ == '__main__':
# 	main()

