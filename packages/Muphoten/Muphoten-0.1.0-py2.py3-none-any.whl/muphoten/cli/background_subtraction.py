#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 18:11:45 2021

@author: duverne, IJClab, Orsay, duverne@protonmail.com
"""

import argparse
import sys
import os
import warnings
from astropy.io import fits
import hjson

from muphoten.background import sub_background
from muphoten.utils import (list_files, get_filename, make_results_dir,
                            getTel, load_config)

warnings.simplefilter(action="ignore", category=FutureWarning)

"""Muphoten script for background substraction."""

def main():
    """Muphoten background subtraction."""

    telescope_list = getTel()

    parser = argparse.ArgumentParser(description="Subtracts background in fits\
                                     images using photutils. Can ave the\
                                     background subtracted images or the\
                                     background image.")

    parser.add_argument("--images",
                        required=True,
                        type=str,
                        help="Path where the images are stored. ")

    parser.add_argument("--telescope",
                        choices=telescope_list,
                        required=True,
                        type=str,
                        help="Alias for the available telescopes.")

    parser.add_argument("--keep-old",
                        dest="keep",
                        required=False,
                        action="store_true",
                        help="Keep previous results")

    parser.add_argument("--skip-processed",
                        "--skip",
                        dest="skip",
                        required=False,
                        action="store_true",
                        help="Skip already processed files")

    parser.add_argument("--save-png",
                        action="store_true",
                        help="Save the background images as fits and png.\
                              Default : False")

    parser.add_argument("--save-fits",
                        action="store_true",
                        help="Save the background images as fits and png.\
                              Default : False")

    args = parser.parse_args()

    print('Loading configuration for Muphoten,')
    config = load_config(args.telescope)
    mu =config['muphoten']['conf']
    with open(mu) as json_file:
        mu_config = hjson.load(json_file)

    # Loading the image to analyse
    images = list_files(args.images)[0]
    print('Processing {} images'.format(len(images)))
    print(images)
    for i, image in enumerate(images):

        image = make_results_dir(image,
                                directory='background',
                                keep=args.keep,
                                skip=args.skip)
        image_name = get_filename(image)
        print('Subtracting background in image n° {} : {}'.format(i,
                                                                  image_name))
        hdu = fits.open(image)[0]
        data, header = hdu.data, hdu.header

        path2save=os.path.dirname(image)

        sub_background(data, header, image_name,
                       n_sigma=mu_config['bkg_n_sigma'],
                       box_size=mu_config['bkg_box'],
                       bkg_estimator=mu_config['bkg_estimator'],
                       filter_size=mu_config['bkg_filter_size'],
                       path2save=path2save, fits=args.save_fits, png=args.save_png)

    return 0

if __name__ == "__main__":
    main()
