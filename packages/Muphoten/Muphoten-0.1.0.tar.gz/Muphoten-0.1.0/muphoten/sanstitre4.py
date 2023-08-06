#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 18:41:20 2021

@author: duverne, IJClab, Orsay, duverne@protonmail.com
"""

import os
import subprocess
import hjson
import numpy as np
from astropy.io import fits
from astropy import wcs
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u
from muphoten.registration import registration
from muphoten.ps1_survey import ps1_grid, prepare_PS1_sub
from muphoten.utils import ( mkdir_p, rm_p, get_corner_coords, load_config)
# from muphoten.utils import get_phot_cat
from muphoten.psfex import psfex
from muphoten.mosaic import create_mosaic
from muphoten.substraction import hotpants

ima = '/home/duverne/Documents/muphoten/tests/test_im/results/2018cow_20180620_043132_Jun8kevf_kait_B_c/2018cow_20180620_043132_Jun8kevf_kait_B_c.fit'
ref = '/home/duverne/Documents/muphoten/tests/test_im/2018cow_20180807_045955_Aug87fij_kait_B_c_ref.fit'
im_coords = get_corner_coords(ima)
config = load_config('KAIT')
resultDir = '/home/duverne/Documents/muphoten/tests/test_im/results/2018cow_20180620_043132_Jun8kevf_kait_B_c/subtraction'


subfiles = [[ima, ref, None]]


regis_info = registration(subfiles, config, resultDir=resultDir)

sub_files = hotpants(regis_info, config, verbose="QUIET", nb_threads=8)