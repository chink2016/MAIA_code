import os
import numpy as np
import sys
import argparse
import scipy.ndimage
from math import cos
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

def imagegenerator(red_block, green_block, blue_block, output_file_name, width, height):

	band_img = Image.new('RGB',(width,height))
	band_img.putdata(zip(red_block,green_block,blue_block))
	band_img.save(output_file_name)
	band_img.show()
	return band_img

def npzgenerator(red_block, green_block, blue_block, reflectance_block, output_file_name):

	main_arr = np.stack((red_block,green_block,blue_block,reflectance_block),-1)
	np.savez(output_file_name, main_arr)
	return main_arr

def brfconverter( SI, rad_scale, ref_scale, ref_offset,solar_zenith_angle, width, height):
	SI = SI.ravel().reshape(height,width,order='F').ravel()
	solar_zenith_angle = solar_zenith_angle.ravel().reshape(height,width,order='F').ravel()
	solar_zenith_angle = np.radians(solar_zenith_angle)
	ref = np.float_(ref_scale)*(np.float_(SI) - np.float_(ref_offset))
	solar_cos = np.squeeze(np.cos(solar_zenith_angle))
	brf = np.float_(ref)/np.float_(solar_cos)
	brf = np.int_(np.float_(brf)*256/(1.1))
	return brf


def band_extract(band):
	ds = hdf.select(band_ds[band]['ds_name'])
	ds_attr = ds.attributes()
	fill_val = ds_attr['_FillValue']
	bands_str = ds_attr['band_names'].split(',')
	idx = 0

	for i,bands in enumerate(bands_str):
			if bands == band: idx = i

	image_block = ds[idx]
	image_block[image_block > 65000] = 0
	image_block = image_block.ravel().reshape(height,width,order='F').ravel()
	mrange = np.amax(image_block)
	image_block = np.int_((np.float_(np.float_(image_block)/mrange))*256)
	band_img = Image.new('L',(width,height))
	band_img.putdata(image_block)
	band_img.save(output_file_name)
	band_img.show()
	sys.exit(1)

def ref_rad_attr(attributes, idx):
	r_sf = attributes['radiance_scales'][idx]
	r_rs = attributes['reflectance_scales'][idx]
	r_ro = attributes['reflectance_offsets'][idx]
	return (r_sf,r_rs,r_ro)

def main():

	global width
	global height
	parser = argparse.ArgumentParser(description='This will produce a cloud mask image in grayscale')
	parser.add_argument('-i','--input',required=True,help='Input hdf file name')
	parser.add_argument('-b','--band',default=-1,help='Input band number')
	parser.add_argument('-s','--solar_zenith',required=True,help='Input solar_zenith file name')
	parser.add_argument('-o','--output',required=True,help='Output image file name')
	parser.add_argument('-c','--crop',action='store_false',help='If you want it to be true size')
	parser.add_argument('-npz','--npz',action='store_true',help='Generates npz file')
	parser.add_argument('-img','--img',action='store_true',help='Generates image file')
	args = parser.parse_args()

	hdf_file_name = args.input
	output_file_name = args.output


	hdf = SD(hdf_file_name)

	band = int(args.band)
	if band != -1:
		if(band_ds[band] == 0): 
			print "\nUnavailable band number. Band numbers that are available: 1, 2, 4, 6, 7, 15, 16, 19, and 26"
			sys.exit(1)
		band_extract(band)


	solar_zenith_file = SD(args.solar_zenith)

	solar_ds = solar_zenith_file.select('SolarZenith')[:,:]

	solar_ds = np.float_(solar_ds)*np.float_(0.01)


	red_ds = hdf.select(band_ds[colors['Red']]['ds_name'])

	greenblue_ds = hdf.select(band_ds[colors['Green']]['ds_name'])

	reflectance_ds = hdf.select('EV_1KM_RefSB')

	red_ds_attr = red_ds.attributes()

	greenblue_ds_attr = greenblue_ds.attributes()

	
	red_idx = 0
	green_idx = 1
	blue_idx = 0

	red_attr = ref_rad_attr(red_ds_attr,red_idx)
	green_attr = ref_rad_attr(greenblue_ds_attr,green_idx)
	blue_attr = ref_rad_attr(greenblue_ds_attr,blue_idx)


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
		solar_ds = solar_ds[w_l:w_r,h_l:h_r]
		width = 400
		height = 400


	red_block[red_block > 65000] = 0
	green_block[green_block > 65000] = 0
	blue_block[blue_block > 65000] = 0
	reflectance_block[reflectance_block > 65000] = 0
	solar_ds[solar_ds > 65000] = 0

	red_brf = brfconverter(red_block,red_attr[0],red_attr[1], red_attr[2], solar_ds, width, height)
	green_brf = brfconverter(green_block, green_attr[0], green_attr[1], green_attr[2], solar_ds, width, height)
	blue_brf = brfconverter(blue_block, blue_attr[0], blue_attr[1], blue_attr[2], solar_ds, width, height)



	if args.npz == True:
		reflectance_block = reflectance_block.ravel().reshape(height,width,order='F').ravel()
		return npzgenerator(red_brf, green_brf, blue_brf, reflectance_block, output_file_name)

	if args.img == True:
		return imagegenerator(red_brf, green_brf, blue_brf, output_file_name, width, height)


if __name__ == '__main__':
	main()
