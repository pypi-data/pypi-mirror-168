#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Wed Feb 10 18:02:32 2021

@author: duverne, corre
"""

import argparse
import warnings
import glob, os

from astropy.io import fits

from muphoten.utils import (load_config, list_files, 
                            make_results_dir,
                            clean_outputs, getpath, getTel, get_filename)
from muphoten.sanitise import sanitise_fits
from muphoten.subtraction import subtraction
from muphoten.astrometry import astrometric_calib
from muphoten.plot_image import plot_image

# clean_folder, cut_image
warnings.simplefilter(action="ignore", category=FutureWarning)

"""Muphoten script for sutracting template image with HOTPANTS."""

def main():

    path_muphoten = getpath()

    telescope_list = getTel()

    parser = argparse.ArgumentParser(
        usage="usage: %(prog)s data [data2 ... dataN] [options]",
        description="Subtraction with HOTPANTS in astronomical images.")

    parser.add_argument(
        "--images",
        required=True,
        type=str,
        help="Base path for the images to analyse.")

    parser.add_argument(
        "--skip-processed",
        "--skip",
        dest="skip",
        required=False,
        action="store_true",
        help="Skip already processed files")

    parser.add_argument(
        "--keep-processed",
        "--keep",
        dest="keep",
        required=False,
        action="store_true",
        help="Skip already processed files")

    parser.add_argument(
        "--telescope",
        dest="telescope",
        choices=telescope_list,
        required=True,
        type=str,
        help="Alias for the available telescopes.")

    parser.add_argument(
        "--astrometry",
        dest="doAstrometry",
        required=False,
        default="scamp",
        choices=["no", "scamp"],
        help="Whether to perform astrometric calibration, with scamp. ")
    
    parser.add_argument(
        "--sub",
        dest="doSub",
        # choices=["ps1", "path to reference image"],
        default="ps1",
        required=False,
        type=str,
        help="Whether to perform astrometric calibration, with ps1 images "
             'or user provided reference image. Type "ps1" for PS1 reference '
             'image or provide the path to your reference image.')

    parser.add_argument(
        "--ps1-method",
        dest="ps1_method",
        required=False,
        default="mosaic",
        choices=["mosaic", "individual"],
        type=str,
        help="When substracting images using Pan-STARRS reference images, "
             "there 2 options, either create a mosaic of all PS1 image and "
             "substract or do the substraction individually for each PS1 "
             "image. In the latter case, your image is cut to match the "
             "PS1 image. (Default: mosaic)")

    parser.add_argument(
        "--mosaic",
        dest="doMosaic",
        action="store_true",
        help="Whether to combine the individual frames into a common mosaic "
             "when `ps1_method` is set to `individual`. (Default: not set)")

    parser.add_argument(
        "--output-data-level",
        dest="outLevel",
        required=False,
        type=int,
        default=0,
        choices=[0, 1, 2],
        help="Number of output files that are kept after the process. "
             "0: minimum, 2: maximum"
             "(Default: 0)")

    parser.add_argument(
        "--conv-filter",
        dest="convFilter",
        required=False,
        default="default",
        type=str,
        help="Corresponds to FILTER_NAME keyword for sextractor "
             "(without .conv)."
             "\nDifferent filter available listed here: %s"
        % path_muphoten + "/config/conv_kernels/"
             "\n(Default: default)")

    parser.add_argument(
        "--verbose",
        dest="verbose",
        required=False,
        default="NORMAL",
        choices=["QUIET", "NORMAL", "FULL", "LOG"],
        type=str,
        help="Level of verbose, according to astromatic software. ")
    
    # parser.add_argument(
    #     "--quadrants",
    #     dest="quadrants",
    #     required=False,
    #     default=1,
    #     type=int,
    #     help="Number of quadrants the image is divided. "
    #          "(Default: 1)")

    args, filenames = parser.parse_known_args()

    # Nb_cuts = (args.quadrants, args.quadrants)

    # Load config files for a given telescope
    print('Loading configuration')
    config = load_config(args.telescope, args.convFilter)

    print('Looking for the images')
    images = list_files(args.images, get_subdirs=False)
    print(images)

    if (args.doAstrometry != "no") and (args.doSub != "ps1"):
        astrometric_calib(args.doSub,
                          config,
                          soft=args.doAstrometry,
                          verbose=args.verbose,
                          accuracy=0.15,
                          itermax=10)

    for i, image in enumerate(images):
        print(image)
        image = make_results_dir(image,
                                 directory='subtraction',
                                 keep=args.keep,
                                 skip=args.skip)
        image_name = get_filename(image)

        if not image:
            print("{} is already processed, skipping. \n".format(image_name))
            continue

        print("Sanitise header and data of {}.\n".format(image_name))
        sanitise_fits(image)

        # # Cut image into several quadrants if required
        # # And create table with filename and quadrant ID
        # image_table = cut_image(
        #     filename,
        #     config,
        #     Nb_cuts=Nb_cuts,
        #     doAstrometry=args.doAstrometry
        # )

        if args.doAstrometry != "no":
            astrometric_calib(image,
                              config,
                              soft=args.doAstrometry,
                              verbose=args.verbose,
                              accuracy=0.15,
                              itermax=10)

        subtraction(image,
                     args.doSub,
                     config,
                     soft="hotpants",
                     method=args.ps1_method,
                     doMosaic=args.doMosaic,
                     verbose=args.verbose,
                     outLevel=args.outLevel,
                     nb_threads=8)
        # clean output files
        clean_outputs(image, args.outLevel)

        image_rep = os.path.dirname(image)
        sub_rep = os.path.join(image_rep, 'subtraction')
        sub = glob.glob(sub_rep + '/*.fit*')
        hdu = fits.open(sub[0])[0]
        data = hdu.data
        plot_image(data, path2save=sub_rep, name='/sub_im')


if __name__ == "__main__":
    main()
