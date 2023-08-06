#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 00:35:04 2021

@author: duverne, IJClab, Orsay, duverne@protonmail.com
"""

import argparse, os, hjson, warnings
from astropy.io import fits
from astropy.wcs import WCS, FITSFixedWarning
from astropy.table import Table
from muphoten.utils import (getTel, make_results_dir, get_filename,
                            list_files, load_config, set_results_table)
from muphoten.sanitise import sanitise_fits
from muphoten.catalog import get_filter
from muphoten.mag_lim import compute_mag_lim

warnings.filterwarnings("ignore", category=FITSFixedWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

"""Muphoten script for limit magnitude estimation."""


def main():

    """Console script for muphoten."""
    # path_muphoten = getpath()
    telescope_list = getTel()
    parser = argparse.ArgumentParser(description="Performing photometry of\
                                     transient objects.")

    parser.add_argument("--images",
                        dest="images",
                        required=True,
                        type=str,
                        help="Path to images.")

    parser.add_argument("--outname",
                        required=True,
                        type=str,
                        help="Name of the output file.")

    parser.add_argument("--telescope",
                        dest="telescope",
                        choices=telescope_list,
                        type=str,
                        help="Telescope that acquired the images.")

    parser.add_argument("--precision",
                        default=0.2,
                        type=float,
                        help="Bin size for the estimation")

    parser.add_argument("--lower-mag",
                        default=15.,
                        type=float,
                        help="Lower bound for the limit magnitude.")

    parser.add_argument("--upper-mag",
                        default=22.,
                        type=float,
                        help="Upper bound for the limit magnitude.")

    parser.add_argument("--threshold",
                        default=0.5,
                        type=float,
                        help="Threshold where the limit magnitude is\
                              considered reached")
    
    args = parser.parse_args()
    
    print('Loading configuration for Muphoten,')
    config = load_config(args.telescope)
    mu = config['muphoten']['conf']
    with open(mu) as json_file:
        mu_conf = hjson.load(json_file)

    images = list_files(args.images, get_subdirs=False)
    results_file = os.path.join(args.images, 'results')

    col_name = ['filename',
                'telescope',
                'filter',
                'time',
                'limit_magnitude',
                'precision',
                'interval_inf',
                'interval_sup']
    res = set_results_table(col_name, len(images))

    for i, image in enumerate(images):
        print(image)
        image = make_results_dir(image,
                                 directory='mag_lim')
        print(image)
        image_rep = os.path.dirname(image)
        calib_rep = os.path.join(image_rep, 'mag_lim')

        image_name = get_filename(image)
        res['filename'][i] = image_name
        path_ratio = os.path.join(calib_rep, 'ratio')
        path_histo = os.path.join(calib_rep, 'histogram')
        print('Processing image n° {} : {}'.format(i, image_name))
        print('Sanitising header')
        # sanitise_fits(image)
        hdu = fits.open(image)[0]
        data, header = hdu.data, hdu.header
        wcs_data = WCS(header)

        if 'TELESCOP' in header.keys():
            res['telescope'][i] = header['TELESCOP']
        else:
            res['telescope'][i] = args.telescope

        # Getting different useful informations : band, MJD,
        # catalog for calibration.
        res['time'][i] = header.get('MJD-OBS')

        band = get_filter(header)
        res['filter'][i] = band

        print('Estimating the limit magnitude in {}'.format(image_name))
        interval = [args.lower_mag, args.upper_mag]
        lim_mag, precision = compute_mag_lim(data, wcs_data, band, mu_conf,
                                             precision=args.precision,
                                             interval=interval,
                                             threshold=args.threshold,
                                             path_ratio=path_ratio,
                                             path_histo=path_histo)
        res['limit_magnitude'][i] = lim_mag
        res['precision'][i] = precision
        res['interval_inf'][i] = interval[0]
        res['interval_sup'][i] = interval[1]
        Table(res[i]).write(calib_rep + '/mag_lim_results.dat',
                     format='ascii.commented_header',
                     overwrite=True)

    res.write(results_file + '/' + args.outname,
              format='ascii.commented_header',
              overwrite=True)
    return 0

if __name__ == "__main__":
    main()
