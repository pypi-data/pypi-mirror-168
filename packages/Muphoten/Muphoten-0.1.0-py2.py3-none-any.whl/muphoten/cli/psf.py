#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:30:32 2021

@author: duverne, IJClab, Orsay, duverne@protonmail.com

Author: David Corre, Orsay, France, corre@iap.fr

"""

import argparse
import warnings
import os

from muphoten.utils import (
    load_config,
    list_files,
    make_results_dir,
    getpath,
    getTel)    
from muphoten.psfex import psfex

warnings.simplefilter(action="ignore", category=FutureWarning)


def main():

    path_muphoten = getpath()
    telescope_list = getTel()

    parser = argparse.ArgumentParser(
        usage="usage: %(prog)s data [data2 ... dataN] [options]",
        description="Compute PSF of astronomical images."
    )

    parser.add_argument(
        "--images",
        dest="path_image",
        required=False,
        type=str,
        help="Base path to repertory containing the images to analyse. "
    )
    
    # parser.add_argument(
    #     "--results",
    #     dest="path_results",
    #     required=False,
    #     type=str,
    #     default='muphoten_results',
    #     help="Base path to store the results. "
    #          "(Default: muphoten_results)"
    # )

    parser.add_argument(
        "--keep-old",
        "--keep",
        dest="keep",
        required=False,
        action="store_true",
        help="Keep previous results"
    )

    parser.add_argument(
        "--skip-processed",
        "--skip",
        dest="skip",
        required=False,
        action="store_true",
        help="Skip already processed files"
    )

    parser.add_argument(
        "--telescope",
        dest="telescope",
        choices=telescope_list,
        required=True,
        type=str,
        help="Alias for the available telescopes.",
    )

    parser.add_argument("--conv-filter",
                        dest="convFilter",
                        required=False,
                        default="default",
                        type=str,
                        help="Corresponds to FILTER_NAME keyword for sextractor"
                             "(without .conv)."
                             "\nDifferent filter available listed here: %s"
                        % path_muphoten + "/config/conv_kernels/"
                             "\n(Default: default)",)

    parser.add_argument(
        "--use-weight",
        dest="useweight",
        action="store_true",
        help="If set, use weight map. "
             "Must be same name as image with .weight.fits extension. "
             "(Default: False)",
    )

    parser.add_argument(
        "--verbose",
        dest="verbose",
        required=False,
        default="NORMAL",
        choices=["QUIET", "NORMAL", "FULL", "LOG"],
        type=str,
        help="Level of verbose, according to astromatic software. "
             "(Default: NORMAL)",
    )

    args = parser.parse_args()
    print(args.telescope)
    # Load config files for a given telescope
    config = load_config(args.telescope, args.convFilter)

    filenames = list_files(args.path_image)[0]
    print('Processing {} images'.format(len(filenames)))

    for image in filenames:

        filename = make_results_dir(image,
                                    directory='psf',
                                    keep=args.keep,
                                    skip=args.skip)
        print(filename)
        if not filename:
            print("%s is already processed, skipping. \n" % image)
            continue

            if not os.path.exists(filename):
                print("Pre-processing failed")
                continue

        psfex(filename, config, useweight=args.useweight,
              verbose=args.verbose, outLevel=2)


if __name__ == "__main__":
    main()
