#!/usr/bin/env python

import os
import numpy as np
import sys
from pyhdf.SD import *
import argparse

w = 2030
h = 1354

w_n = 400
h_n = 400

w_l = w/2 - 200
w_r = w_l + 400

h_l = h/2 - 200
h_r = h_l + 400


def main():

	parser = argparse.ArgumentParser(description='This will produce a cloud mask image in grayscale')
	parser.add_argument('-i','--input',required=True,help='Input hdf file name')
	parser.add_argument('-o','--output',required=True,help='Output npz file name')

	parser.add_argument('-c','--crop',action='store_false',help='If you want it to be true size')
	args = parser.parse_args()

	#Obtaining file name
	hdf_file_name = args.input
	npz_file_name = args.output

	hdf = SD(hdf_file_name)

	cld_mask = hdf.select('Cloud_Mask_1km')

	# MOD06 section
	if args.crop == False:
		cld_ds_0 = cld_mask[:,:,0]
	else:
		cld_ds_0 = cld_mask[w_l:w_r,h_l:h_r,0]

	cld_img = cld_ds_0
	cld_img = (np.int_(cld_img) >> 1) & 0x03
	np.savez(npz_file_name,cloud_mask = cld_img)


if __name__ == '__main__':
	main()

