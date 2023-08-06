#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:13:10 2020

@author: duverne
"""

from astropy.io import fits
from astropy.time import Time  
import glob

def add_filter(fits_file, band):
    
    with fits.open(fits_file, mode = 'update') as hdul:
        hdul[0].header.append(('FILTER', band))

def add_MJD(fits_file, mjd):

    with fits.open(fits_file, mode = 'update') as hdul:
        hdul[0].header.append(('MJD-OBS', mjd))


file = '/home/duverne/gmadet/final_kepd/gmadet_results/ATLAS18qqn_0_g_20180620_043424.017130_o/ATLAS18qqn_0_g_20180620_043424.017130_o.fits'

# list_file = glob.glob('/home/duverne/Documents/AT2018cow_data/kped/g_band'+'/*')
list_file = glob.glob('/media/duverne/DISQUE ESSB/AT2018cow/kepd/r_band'+'/*')
list_file=[file for file in list_file if '_psf' not in file and 'sub_' not in file]

for file in list_file:

    # add_filter(file, 'g')
    name = file.split('/')[-1]
    obs = name.split('_')
    
    y = obs[3][0:4]
    m = obs[3][4:6]
    d = obs[3][6:8]
    time = y + '-' + m + '-' + d +'T'
    
    h = obs[4][0:2]
    mi = obs[4][2:4]
    sec = obs[4][4:]
    time+=h+':'+mi+':'+sec
    time_utc = Time(time, format='isot')
    mjd = time_utc.mjd
    print(mjd)
    add_MJD(file, mjd)