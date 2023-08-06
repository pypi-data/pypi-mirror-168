#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 01:39:48 2021

@author: corre, duverne, IJClab, Orsay, duverne@protonmail.com
"""

import numpy as np
from astropy.io import fits
from astropy.time import Time, TimeDelta

def sanitise_headers(filename, fix=False):
    """
    Keep only important keywords.
    Helps not to crash when headers are not well formated.
    """

    #  Need to keep minimum information about astrometric
    #  calibration for initialising scamp
    #  List of official keywords:
    #  https://heasarc.gsfc.nasa.gov/docs/fcg/standard_dict.html
    # Other keywords commonly used:
    #  https://heasarc.gsfc.nasa.gov/docs/fcg/common_dict.html
    #  Keywords not present in this list are discarded.
    keywords_to_keep = [
        "SIMPLE",
        "BITPIX",
        "NAXIS",
        "NAXIS1",
        "NAXIS2",
        "EXTEND",
        "DATE-OBS",
        "DATE-END",
        "TELESCOP",
        "INSTRUME",
        "OBJECT",
        "EXPTIME",
        "FILTER",
        "GAIN",
        "SATURATE",
        "EQUINOX",
        "EPOCH",
        # "RADESYS",
        "CTYPE1",
        "CTYPE2",
        "CUNIT1",
        "CUNIT2",
        "CRVAL1",
        "CRVAL2",
        "CRPIX1",
        "CRPIX2",
        "CD1_1",
        "CD1_2",
        "CD2_1",
        "CD2_2",
        "CDELT1",
        "CDELT2",
        "CROTA1",
        "CROTA2",
        "BSCALE",
        "BZERO",
        "BUNIT",
        "AIRMASS",
        "END",
        "MJD-OBS",
        'JD',
        'DATE',
        'BJD-OBS',
        'HJD-OBS',
        'JD-OBS',
        'OBSDATE',
        'TELESCOPE',
        'INSTFILT']
    hdulist = fits.open(filename)
    # Verify and try to fix issue with fits standard
    if fix: 
        hdulist.verify("fix")
    hdr = hdulist[0].header
    keywords2delete = []
    for key, value in hdr.items():
        #  if EXPOSURE keyword present, rename it EXPTIME
        if key == "EXPOSURE":
            #  check if EXPTIME exists, otherwise create it
            try:
                if hdr["EXPTIME"]:
                    pass
            except BaseException:
                hdr["EXPTIME"] = value
                #  if EXPOSURE keyword present, rename it EXPTIME
        if key == "FILTERS":
            #  check if FILTER exists, otherwise create it
            try:
                if hdr["FILTER"]:
                    pass
            except BaseException:
                hdr["FILTER"] = value

        if key not in keywords_to_keep:
            keywords2delete.append(key)
    keywords2delete = np.unique(keywords2delete)
    for key in keywords2delete:
        del hdr[key]
    if 'EXPTIME' not in hdr:
        start, end = Time(hdr['DATE-OBS']), Time(hdr['DATE-END'])
        hdr["EXPTIME"] = int(TimeDelta([end.jd-start.jd],
                                       format='jd').to_value(format='sec')[0])
        # Try to set the exposure time if not in headern with start and
        # end time in the header.

    if 'FILTER' not in hdr:
        if "INSTFILT" in hdr:
            hdr["FILTER"] = hdr["INSTFILT"]
        else:
            raise KeyError('No filter found in {}.'
                           'Use the set-band command to modify the'
                           'header.'.format(filename))
    hdulist.writeto(filename, overwrite=True)

def sanitise_data(filename):
    """
    Make sure that the data are in the primary hdu.
    Otherwise some astromatic softs are not working properly.
    Other solution would be to check astromatic soft config.
    """
    # Make sure to use only the Primary hdu.
    # sextractor, scamp seems to crash otherwise.
    hdul = fits.open(filename)
    # hdul.verify('fix')
    if len(hdul) > 1:
        print("More than one HDU in fits file.")
        print("Keeping only the PrimaryHDU.")
        newhdu = fits.PrimaryHDU()
        newhdu.data = hdul[0].data
        newhdu.header = hdul[0].header
        newhdulist = fits.HDUList([newhdu])
        newhdulist.writeto(filename, overwrite=True)
        hdul.close()

def sanitise_time(filename):
    """
    Set the MJD-OBS keyword in the header for the analysis

    Parameters
    ----------
    filename : path.
        The path to an image to check its header and add
        the keyword if necessary.

    Returns
    -------
    None.

    """
    hdulist = fits.open(filename)
    header = hdulist[0].header
    times = ['JD',#'DATE',
             'DATE-OBS','OBSDATE',
             'BJD-OBS', 'HJD-OBS', 'JD-OBS']
    if 'MJD-OBS' not in header:
        for time in times:
            if time in header:
                try:
                    MJD = Time(header[time]).mjd
                    header["MJD-OBS"] = "{}".format(MJD)
                    print(MJD)
                    break
                except ValueError:
                    continue
        hdulist.writeto(filename, overwrite=True)

def add_filter(filename, band):
    """
    Add the FILTER keyword in header.

    Parameters
    ----------
    fits_file : Path.
        Image in which the keyword must be added.
    band : str
        Filter that has been used to acquire the image.

    Returns
    -------
    None.

    """    
    with fits.open(filename, mode = 'update') as hdul:
        hdul[0].header.append(('FILTER', band))

def add_observer(filename, tel):
    """
    Add the observer in the fits header

    Parameters
    ----------
    filename : fits file
        File to be modified..
    tel : str
        Name opf the observer
    Returns
    -------
    None.

    """
    with fits.open(filename, mode = 'update') as hdul:
        hdul[0].header.append(('TELESCOP', tel))

def sanitise_fits(filename):
    """Call function to sanitise fits headers and data"""
    try:
        sanitise_headers(filename)
    except Exception:
        sanitise_headers(filename, fix=True)
    sanitise_headers(filename)
    sanitise_time(filename)
    sanitise_data(filename)
