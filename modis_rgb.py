import os
import numpy as np
import sys
import argparse
from pyhdf.SD import *
from PIL import Image

band_ds = 	[0	,	{'ds_name': 'EV_250_Aggr1km_RefSB', 'mrange': 17730},	{'ds_name': 'EV_250_Aggr1km_RefSB','mrange':17730},	{'ds_name': 'EV_500_Aggr1km_RefSB','mrange':18314},	{'ds_name': 'EV_500_Aggr1km_RefSB','mrange':18314},
			 0,		{'ds_name': 'EV_500_Aggr1km_RefSB'}, 	{'ds_name': 'EV_500_Aggr1km_RefSB'},	0,	0,
			 0,	0,	0,	0,	0,
			 {'ds_name': 'EV_1KM_RefSB'}, 	{'ds_name': 'EV_1KM_RefSB'}, 	0,	0, 	{'ds_name': 'EV_1KM_RefSB'},
			 0,	0,	0,	0,	0,	
			 0,	{'ds_name': 'EV_1KM_RefSB'}]

colors = {'Red':1, 'Green':4, 'Blue':3}

width = 2030
height = 1354

w_l = width/2 - 200
w_r = w_l + 400

h_l = height/2 - 200
h_r = h_l + 400

def main():

	global width
	global height
	parser = argparse.ArgumentParser(description='This will produce a cloud mask image in grayscale')
	parser.add_argument('-i','--input',required=True,help='Input hdf file name')
	parser.add_argument('-o','--output',required=True,help='Output image file name')

	parser.add_argument('-c','--crop',action='store_false',help='If you want it to be true size')
	args = parser.parse_args()

	hdf_file_name = args.input
	output_file_name = args.output


	hdf = SD(hdf_file_name)


	red_ds = hdf.select(band_ds[colors['Red']]['ds_name'])

	greenblue_ds = hdf.select(band_ds[colors['Green']]['ds_name'])

	reflectance_ds = hdf.select('EV_1KM_RefSB')

	red_ds_attr = red_ds.attributes()

	greenblue_ds_attr = greenblue_ds.attributes()
	
	red_idx = 0
	green_idx = 1
	blue_idx = 0

	r_sf = red_ds_attr['radiance_scales'][red_idx]
	g_sf = greenblue_ds_attr['radiance_scales'][green_idx]
	b_sf = greenblue_ds_attr['radiance_scales'][blue_idx]

	valid_r = float(red_ds_attr['valid_range'][1])*b_sf
	valid_g = float(greenblue_ds_attr['valid_range'][1])*b_sf
	valid_b = float(greenblue_ds_attr['valid_range'][1])*b_sf

	if(args.crop == False):
		red_block = red_ds[red_idx]
		green_block = greenblue_ds[green_idx]
		blue_block = greenblue_ds[blue_idx]
		reflectance_block = reflectance_ds[14]
	else:
		red_block = red_ds[red_idx][w_l:w_r,h_l:h_r]
		green_block = greenblue_ds[green_idx][w_l:w_r,h_l:h_r]
		blue_block = greenblue_ds[blue_idx][w_l:w_r,h_l:h_r]
		reflectance_block = reflectance_ds[14][w_l:w_r,h_l:h_r]
		width = 400
		height = 400


	red_block[red_block > 65000] = 0
	green_block[green_block > 65000] = 0
	blue_block[blue_block > 65000] = 0
	reflectance_block[reflectance_block > 65000] = 0

	red_width = green_width = blue_width = reflectance_width = width
	red_height = green_height = blue_height = reflectance_height = height

	red_block = np.float_((np.float_(red_block))*r_sf)
	green_block = np.float_((np.float_(green_block))*g_sf)
	blue_block = np.float_((np.float_(blue_block))*b_sf)

	red_block = np.int_((np.float_(np.float_(red_block)/valid_r))*256)
	green_block = np.int_((np.float_(np.float_(green_block)/valid_g))*256)
	blue_block = np.int_((np.float_(np.float_(blue_block)/valid_b))*256)

	main_arr = np.stack((red_block,green_block,blue_block,reflectance_block),-1)
	np.savez(output_file_name, main_arr)


if __name__ == '__main__':
	main()
