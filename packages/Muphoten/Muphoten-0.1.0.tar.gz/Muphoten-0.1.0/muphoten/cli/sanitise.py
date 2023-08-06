#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 22:32:34 2021

@author: duverne, IJClab, Orsay, duverne@protonmail.com
"""

import sys
import argparse
from muphoten.sanitise import add_filter, add_observer, sanitise_fits
from astropy.io import fits
from muphoten.utils import list_files

"""Muphoten script for preparing and making the header right."""

def main():
    
    parser = argparse.ArgumentParser(description="Performing photometry of\
                                     transient objects.")
    
    parser.add_argument("--images",
                    dest="images",
                    required=True,
                    type=str,
                    help="Path to images.")

    parser.add_argument("--telescope",
                    required=True,
                    type=str,
                    help="Telescope that acquired the images.")
    
    parser.add_argument("--filter",
                    required=True,
                    type=str,
                    help="Filter used to acquire the images.")
    args = parser.parse_args()

    images = list_files(args.images, get_subdirs=False)

    for i, image in enumerate(images):
        hdulist = fits.open(image)
        header = hdulist[0].header

        if 'TELESCOPE' not in header.items():
            add_observer(image, args.telescope)
        if 'FILTER' not in header.items():
            add_filter(image, args.filter)
        try:
            sanitise_fits(image)
        except Exception:
            hdulist.verify("fix")
            sanitise_fits(image)

    return 0


if __name__ == "__main__":
    main()
