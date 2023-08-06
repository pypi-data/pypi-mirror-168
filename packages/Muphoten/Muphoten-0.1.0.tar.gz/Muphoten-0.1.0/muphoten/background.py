#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 19:48:07 2020.

@author: duverne
"""
import os
from photutils import (MeanBackground, MedianBackground,
                       ModeEstimatorBackground, MMMBackground,
                       SExtractorBackground, BiweightLocationBackground,
                       Background2D)
from astropy.stats import SigmaClip
from muphoten.utils import createFITS
from muphoten.plot_image import plot_background

"""Muphoten main script for background treatment."""

def background_estimation(data, n_sigma=3.0, box_size=(30, 30),
                          bkg_estimator='sex',
                          filter_size=(3, 3), mask=None):
    """
    Estimation of the background of a fits image with photutils\
    background2D method.

    Parameters
    ----------
    data : data from a .fits file
    n_sigma : sigma level from the median
    box_size : size of the in which the BG is estimated
    bkg_estimator : BG level estimator
    filter_size = size of the filter to use

    Returns :
    -------
    Background object of the data.

    """
    sigma_clip = SigmaClip(sigma=n_sigma)
    if bkg_estimator=='sex':
        bkg_estimator = SExtractorBackground()
    elif bkg_estimator=='mean':
        bkg_estimator = MeanBackground()
    elif bkg_estimator=='median':
        bkg_estimator = MedianBackground()
    elif bkg_estimator=='mode':
        bkg_estimator = ModeEstimatorBackground()
    elif bkg_estimator=='mmm':
        bkg_estimator = MMMBackground()
    elif bkg_estimator=='bi':
        bkg_estimator = BiweightLocationBackground()

    bkg = Background2D(data, box_size=box_size,
                       filter_size=filter_size,
                       sigma_clip=sigma_clip,
                       bkg_estimator=bkg_estimator,
                       coverage_mask=mask)
    return bkg

def bkg_to_array(bkg, rms=True):
    """
    Return an array of the background and an array of its root mean square.

    Parameters
    ----------
    bkg : photutils background object
        An estimation of the background in an image.
    rms : Bool
        if True, compute the rms of the background object

    Returns
    -------
    bkg_array : numpy array
        The background image.
    bkg_rms : numpy array
        The image of the root mean square of the background.

    """
    if rms:
        bkg_array = bkg.background
        bkg_rms = bkg.background_rms
        return bkg_array, bkg_rms
    else:
        bkg_array = bkg.background
        return bkg_array

def subtract(data, bkg):
    """
    Subtraction of the background to an image.

    Parameters
    ----------
    data : numpy array
        Data array.
    bkg : numpy array
        background array.

    Returns
    -------
    data_clean : numpy array
        Background subtracted array

    """
    data_clean = data - bkg
    return data_clean

def sub_background(data, header, image_name, n_sigma=3.0, box_size=(30, 30),
                   bkg_estimator='sex', filter_size=(3, 3), mask=None,
                   path2save=None, fits=None, png=False):
    """
    Perform the background subtraction in a fits image.
    Possible to save the background  and the backgrounds subtracted image
    as a fits images.

    Parameters
    ----------
    data : numpy array
        Image as a array.
    header : astropy header object
        Header of the image.
    image_name : str
        name of the image to save the cleaned image and the background.
    n_sigma : float, optional
        sigma level from the median. The default is 3.0.
    box_size : tuple size 2, optional
        Size of the boxe in which the background is estimated.
        The default is (30, 30).
    bkg_estimator : str, optional
        Estimator name. The default is 'sex'.
    filter_size : tuple size 2, optional
        Size of the filter. The default is (3, 3).
    mask : boolean array, optional
        Array used to mask pixels if some regions
        of the image have to be excludes from
        the estimation of the background.
        The default is None.
    path2save : str, optional
        Path where the are saved. The default is None.
    fits : Bool, optional
        Used to save the background as a fits file. The default is False.
    png : Bool, optional
        Used to save the background as a png file. The default is False.

    Returns
    -------
    data_cleaned : numpy array
        Background subtracted image.
    background_array : numpy array
        Background array.
    background_rms : numpy array
        2D Standard devitation of the image.

    """

    # Computing the background with photutils
    bkg_obj = background_estimation(data,
                                    n_sigma = n_sigma,
                                    box_size = box_size,
                                    bkg_estimator=bkg_estimator,
                                    filter_size=filter_size,
                                    mask=mask)

    # Convert the Background object into a numpy array
    background_array, background_rms = bkg_to_array(bkg_obj, rms=True)

    # Subtracting the background to the image
    data_cleaned = data - background_array

    # Save clean image if required
    if path2save is not None:
        background_filename = os.path.join(path2save,
                                           'background/background_' +
                                           image_name)
        if fits:
            clean_filename = os.path.join(path2save,
                                          'clean_' + image_name + '.fits')
            createFITS(data_cleaned, header, filename=clean_filename)
    
        # Save background image

            createFITS(background_array, header,
                       filename=background_filename+'.fits')
    
        # Save RMS image
            RMS_filename = os.path.join(path2save,
                                        'background/rms_' + image_name)
            createFITS(background_rms, header,
                       filename=RMS_filename+'.fits')

        if png:
            plot_background(data, background_array, dif=False,
                            save=True, path=background_filename+'.png')

    return data_cleaned, background_array, background_rms
