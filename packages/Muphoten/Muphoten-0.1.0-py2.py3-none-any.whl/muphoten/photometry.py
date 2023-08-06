#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 00:09:43 2020.

@author: duverne
"""

import warnings
import numpy as np
from astropy.stats import (gaussian_fwhm_to_sigma)
from astropy.convolution import Gaussian2DKernel
from astropy import units as u
# from astropy.table import vstack, hstack, join
# from astropy import units as u, coordinates as coord
from astropy.wcs import WCS, FITSFixedWarning
from photutils import (detect_sources, deblend_sources, source_properties,
                       SkyEllipticalAperture, aperture_photometry,
                       SkyCircularAperture, CircularAperture,
                       EllipticalAperture)
from photutils.utils import calc_total_error

warnings.filterwarnings("ignore", category=FITSFixedWarning)


def masking(image, coordinate, header, mask_size):
    """
    Create a square mask around a position.

    Parameters
    ----------
    image : numpy array
        Image data.
    coordinate : list of length 2
        position in radec for the center of the mask.
    header : header object
        header of the fits file.
    mask_size : int
        size of the mask in pixel.

    Returns
    -------
    mask : boolean numpy array
        boolean mask.

    """
    w = WCS(header)
    coord_image = w.all_world2pix(coordinate, 1)
    shape = np.shape(image)
    xs = coord_image[0][0]
    ys = coord_image[0][1]
    mask = np.ones_like(image, dtype=bool)
    yo = max(int(ys) - int(mask_size), 0)
    y1 = min(int(ys) + int(mask_size), shape[0])
    xo = max(int(xs) - int(mask_size), 0)
    x1 = min(int(xs) + int(mask_size), shape[1])
    print(xo, x1)
    print(yo, y1)
    mask[yo:y1, xo:x1] = False

    return mask


def source_detection(data, background_array, background_rms, n_sigma=3.0,
                     deblend=True, mask=None, threshold_level=2.,
                     npixels=5, contrast=0.001):
    """
    Detect the sources in an image.

    Parameters
    ----------
    data : numpy array
        Image data NOT background subtracted.
    background_array : numpy array
        Background in the image data.
    background_rms : numpy array
        Background RMS in the image data.
    n_sigma : int, optional
        FWHM of the gaussian in pixel used to filter the data.
        The default is 3.0.
    deblend : Boolean, optional
        Deblend or not the sources. The default is True.
    mask : numpy array, optional
        A mask to define where to search for sources. The default is None.
    threshold_level : Float, optional
        Level to above the background to define a source.
        The default is 2. sigma.
    npixels : int, optional
        Number of connected pixels to define a source. The default is 5.
    contrast : Float, optional
        Fraction of the total source flux that a local peak must have to be
        considered as a separate object. The default is 0.001.

    Returns
    -------
    Photutils Segmentation object
        A segmentation image containing the detected sources in the image.

    """
    # WARNING data MUST NOT BE background subtracted
    threshold = background_array + (threshold_level*background_rms)
    sigma = n_sigma * gaussian_fwhm_to_sigma
    kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
    kernel.normalize()
    if mask is not None:
        segm = detect_sources(data, threshold, filter_kernel=kernel,
                              npixels=npixels, mask=mask)
    else:
        segm = detect_sources(data, threshold, npixels=npixels,
                              filter_kernel=kernel)
    if deblend:
        if segm is not None:
            segm = deblend_sources(data, segm, npixels=npixels,
                                   filter_kernel=kernel,
                                   contrast=contrast)
    return segm


def Fixed_Photometry(raw_data, sub_data, segmentation, header, radius,
                     background_array, background_rms, wcs=None):
    """

    """
    try:
        time = float(header.get("EXPOSURE"))
    except Exception:
        try:
            time = float(header.get("EXPTIME"))
        except Exception:
            time = 1.0

    error = calc_total_error(raw_data,
                             background_rms,
                             effective_gain=time)
    cat = source_properties(sub_data, segmentation,
                            background=background_array,
                            error=error, wcs=wcs)
    columns = ['id', 'xcentroid', 'ycentroid', 'sky_centroid',
               'background_sum']#, 'centroid']
    table = cat.to_table(columns=columns)
    table['xcentroid'].info.format = '.4f'  # optional format
    table['ycentroid'].info.format = '.4f'
    apertures = SkyCircularAperture(table['sky_centroid'], r=radius*u.pix)
    photometry = aperture_photometry(sub_data, apertures.to_pixel(wcs))
    table['aperture'] = apertures
    table['aperture_sum'] = photometry['aperture_sum']
    table['Magnitude'] = -2.5 * np.log10(table['aperture_sum'])
    table['Magnitude'].info.format = '.4f'
    table['idx'] = np.arange(len(table))

    return table


def Kron_Photometry(raw_data, sub_data, segmentation, header,
                    background_array, background_rms, wcs=None):
    """
    Perform photometry in an image.

    Parameters
    ----------
    raw_data : numpy array
        Image data, background NOT subtracted.
    sub_data : numpy array
        Image data, background subtracted.
    segmentation : photutils segmentation object
        Segmented image.
    header : FITS header
        Header of the FITS file.
    background_array : numpy array
        Background of the image.
    background_rms : numpy array
        Background RMS of the image.
    wcs : None or WCS object, optional
        A world coordinate system (WCS) transformation.
        If None, then all sky-based properties will be set to None.

    Returns
    -------
    table : astropy table
        Astropy table with all the informations about the
        sources detected in data.

    """
    # WARNING data MUST NOT BE BG substracted here
    try:
        time = float(header.get("EXPOSURE"))
    except Exception:
        try:
            time = float(header.get("EXPTIME"))
        except Exception:
            time = 1.0

    error = calc_total_error(raw_data,
                             background_rms,
                             effective_gain=time)
    # WARNING data MUST BE BG substracted here
    cat = source_properties(sub_data, segmentation,
                            background=background_array,
                            error=error, wcs=wcs,
                            kron_params=('correct', 2.5, 0.001, 'exact', 5))
    columns = ['id', 'xcentroid', 'ycentroid', 'source_sum', 'area',
               'background_at_centroid', 'background_mean', 'background_sum',
               'sky_centroid', 'kron_aperture', 'kron_flux', 'kron_radius']
    table = cat.to_table(columns=columns)
    table['xcentroid'].info.format = '.4f'  # optional format
    table['ycentroid'].info.format = '.4f'
    table['source_sum'].info.format = '.4f'
    table['background_at_centroid'].info.format = '{:.4f}'  # optional format
    table['background_mean'].info.format = '{:.4f}'
    table['background_sum'].info.format = '{:.4f}'
    table['kron_flux'].info.format = '{:.4f}'
    table['aperture_sum'] = table['kron_flux']
    table['kron_radius'].info.format = '{:.4f}'
    table['aperture'] = table['kron_aperture']
    table['Magnitude'] = -2.5 * np.log10(table['kron_flux'])
    table['Magnitude'].info.format = '.4f'
    table['idx'] = np.arange(len(table))

    return table


def Isophotal_Photometry(raw_data, sub_data, segmentation, header,
                         background_array, background_rms,
                         radius=4, wcs=None):
    """  Compute the instrumental magnitude and several other properties of
    a fits file. This is done using aperture photometry

    Parameters
    ----------
    data : data from a .fits file
    segm_deblend : segmentation image with the sources detected
    header : header of the fits file
    background : estimaton of the background of data
    n_pixels_in : semi-major axis of the inner ellipsis for
    aperture photometry
    n_pixels_out : semi-major axis of the extern ellipsis
    for aperture photometry

    Returns : (background) of the data
    -------
    """

    # WARNING data MUST NOT BE BG substracted here
    try:
        time = float(header.get("EXPOSURE"))
    except Exception:
        try:
            time = float(header.get("EXPTIME"))
        except Exception:
            time = 1.0
    error = calc_total_error(raw_data,
                             background_rms,
                             effective_gain=time)
    cat = source_properties(sub_data, segmentation,
                            background=background_array,
                            error=error, wcs=wcs)
    columns = ['id', 'xcentroid', 'ycentroid',
               'sky_centroid', 'background_sum',
               'semimajor_axis_sigma', 'semiminor_axis_sigma', 'orientation']
    table = cat.to_table(columns=columns)
    table['xcentroid'].info.format = '.4f'  # optional format
    table['ycentroid'].info.format = '.4f'
    apertures = []
    photometry = []
    for i in range(len(table)):
        elli = SkyEllipticalAperture(positions=table['sky_centroid'][i],
                                     a=table['semiminor_axis_sigma'][i]*radius,
                                     b=table['semimajor_axis_sigma'][i]*radius,
                                     theta=table['orientation'][i])
        apertures.append(elli)
        photometry.append(aperture_photometry(sub_data,
                                              elli.to_pixel(wcs))['aperture_sum'][0])
    table['aperture'] = apertures
    table['aperture_sum'] = photometry
    table['Magnitude'] = -2.5 * np.log10(table['aperture_sum'])
    table['Magnitude'].info.format = '.4f'
    table['idx'] = np.arange(len(table))

    return table


def get_source(table, coord_source, wcs, col_name='dist'):

    coord_source = wcs.all_world2pix(coord_source, 1)
    table[col_name] = np.sqrt((table['xcentroid']/u.pix -
                               coord_source[0][0])**2
                              + (table['ycentroid']/u.pix -
                                 coord_source[0][1])**2)
    source = table[table[col_name] == min(table[col_name])]
    return source


def Dophot(data, position, wcs, radius=5.0, aperture=None):

    if aperture is None:
        position = wcs.all_world2pix(position, 1)
        aperture = CircularAperture(position, r=radius)
        aper_photo = aperture_photometry(data, aperture)
    else:
        if isinstance(aperture,EllipticalAperture):
            aperture.to_sky(wcs).to_pixel(wcs)
        else:
            aperture = aperture.to_pixel(wcs)
        aper_photo = aperture_photometry(data, aperture)

    return aper_photo['aperture_sum'][0]


def compute_error(table, a, da_2, db_2):

    table['poisson_source_error'] = 2.5/(np.log(10) *
                                         np.sqrt(table['aperture_sum']))
    table['poisson_bkg_error'] = 2.5/(np.log(10) *
                                      np.sqrt(table['background_sum']))
    table['calib_error'] = np.sqrt(table['Magnitude']**2 * da_2 +
                                   db_2 +
                                   a * table['poisson_source_error']**2)

    table['total_error'] = np.sqrt(table['poisson_source_error']**2 +
                                   table['poisson_bkg_error']**2 +
                                   table['calib_error']**2)
    print(table['total_error'])
    return table


def compute_snr(table):

    table['SNR'] = (table['aperture_sum'])/np.sqrt(table['aperture_sum'] +
                                                   table['background_sum'])

    return table
