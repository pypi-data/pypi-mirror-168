#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 16:37:19 2021

@author: duverne
"""

import numpy as np
from astropy import units as u, coordinates as coord
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import matplotlib.pyplot as plt
import muphoten.catalog as cata
from muphoten.background import sub_background
from muphoten.photometry import source_detection
from photutils import source_properties

def get_sky_coord_center(data, wcs):
    """
    Get the center of the image in WCS.

    """

    x_center, y_center = int(np.shape(data)[0]/2), int(np.shape(data)[1]/2)
    coord_center = wcs.all_pix2world(y_center, x_center, 0)
    center = coord.SkyCoord(coord_center[0], coord_center[1],
                            unit=(u.deg, u.deg), frame='icrs')
    return center

def get_fov(data, wcs):
    """
    Get the FoV nformation about the image

    """
    
    size = np.shape(data)
    origin = wcs.all_pix2world(0, 0, 0)
    origin = coord.SkyCoord(origin[0], origin[1],
                            unit=(u.deg, u.deg), frame='icrs')
    
    sup = wcs.all_pix2world(0, size[0], 0)
    sup = coord.SkyCoord(sup[0], sup[1],
                         unit=(u.deg, u.deg), frame='icrs')
    
    inf = wcs.all_pix2world(size[1], 0, 0)
    inf = coord.SkyCoord(inf[0], inf[1],
                         unit=(u.deg, u.deg), frame='icrs')
    
    
    height = origin.separation(sup).deg * u.deg
    width = origin.separation(inf).deg * u.deg
    
    return width, height

def get_region(data, wcs, band='gmag'):
    """
    Get all the objects found in the FoV of the image by Pan-STARRS.

    Parameters
    ----------
    data : numpy array
        The image array.
    wcs : Astropy WCS object
        Astrometry fo the image.
    band : string, optional
        Filter used to acquire the image. The default is 'gmag'.

    Returns
    -------
    region : Astropy array
        The table withthe information about the objects in the FoV.

    """
    
    johnson = ['BMag', 'VMag', 'RMag', 'IMag']
    center = get_sky_coord_center(data, wcs)
    width, height = get_fov(data, wcs)
    Vizier.ROW_LIMIT = 999999999
    Vizier.TIMEOUT=1000.
    region = Vizier.query_region(center, width = Angle(width, "deg"), 
                                 height = Angle(height, "deg"),
                                 catalog = 'II/349/ps1')
    region = region[0]
    region['xcentroid'], region['ycentroid'] = wcs.all_world2pix(region['RAJ2000'],
                                                                 region['DEJ2000'],
                                                                 0)
    if band in johnson:
        region = cata.from_PS2Johnson(band, region)

    if band=='cmag':
        region = cata.from_PS2clear(band, region)

    return region

def detect_objects(data, wcs, band, mu_conf):   
    """
    Find all the objects detected in the image, change the photometric
    system if necessary.

    Parameters
    ----------
    data : numpy array
        image data.
    header : Astropy header
        Image header.
    band : string
        Filter used to acquire the image.
    mu_conf : dictonnary
        Muphoten configuration for the analysis.
    path : path, string
        Path where to save the background image.
    im_name : string
        image name.

    Returns
    -------
    detected_objects : Astropy Table
        Tabme with information about the objects in the FoV.

    """
    
    johnson = ['BMag', 'VMag', 'RMag', 'IMag']
    data_clean, background, rms = sub_background(data, None, None,
                                                 n_sigma=mu_conf['bkg_n_sigma'],
                                                 box_size=mu_conf['bkg_box'],
                                                 bkg_estimator=mu_conf['bkg_estimator'],
                                                 filter_size=mu_conf['bkg_filter_size'])
    #Detection of the sources
    segmentation = source_detection(data, background, rms,
                                    n_sigma=mu_conf['det_n_sigma'],
                                    deblend=mu_conf['det_deblend'],
                                    threshold_level=mu_conf['det_treshold'],
                                    npixels=mu_conf['det_npixels'],
                                    contrast=mu_conf['contrast'])
    cat = source_properties(data_clean, segmentation,
                            background=background,
                            wcs=wcs)

    columns = ['id', 'xcentroid', 'ycentroid', 'sky_centroid']
    table = cat.to_table(columns=columns)
    table['idx'] = np.arange(len(table))
    coord_sources = cata.source_coordinates(table)
    detected_objects = cata.xmatch(coord_sources, 'II/349/ps1', 5.0)
    if band in johnson:
        detected_objects = cata.from_PS2Johnson(band, detected_objects)

    if band=='cmag':
        detected_objects = cata.from_PS2clear(band, detected_objects)

    return detected_objects

def build_ratio(region, detected_objects, band,
                precision=0.2, interval=[15., 22.]):
    """
    Building if the ratio of the detected sources in the image and the objects
    in the catalog.

    Parameters
    ----------
    region : Astropy table
        Table of the sources detected in the FoV by Pan-STARRS.
    detected_objects : Astropy Table
        Table of the sources detected in the image.
    band : string
        Filter used to acquire the image.
    precision : float, optional
        Bin size. The default is 0.2.
    interval : list, optional
        Interval of magnitude where to find the limit magnitude.
        The default is [15., 22.].

    Returns
    -------
    histo_obj : numpy histogram
        Histogram of the sources detected in the image.
    histo_region : numpy histogram
        Histogram of the sources detected in Pan-STARRS.
    mag_lim : numpy histogram
        Limit magnitude of the image.

    """
    
    magmax,  magmin = np.max(region[band]), np.min(region[band])
    rg=(magmin, magmax)
    nbin = int((magmax - magmin)/precision)
    
    mask = (region[band] > interval[0]) & (region[band] < interval[1]) 
    region = region[mask]
    mask = (detected_objects[band] < np.max(region[band])) \
            & (detected_objects[band] > interval[0])
    detected_objects = detected_objects[mask]

    histo_region = np.histogram(region[band], bins= nbin, range=rg)
    histo_obj = np.histogram(detected_objects[band],
                             bins= nbin, range=rg)
    
    mag_lim = np.zeros(np.size(histo_region[0]), dtype=np.float64)
    
    for i in range(len(histo_region[0])):
        if histo_region[0][i] != 0:
            ratio = histo_obj[0][i] / histo_region[0][i]
            if ratio >= 1.0 :
                mag_lim[i] = 1.0
            else:
                mag_lim[i] = ratio

    return histo_obj, histo_region, mag_lim


def do_plot_histo(region, detected_objects, mag_lim, lim, band,
                  precision=0.2, threshold=0.5, name='mag_lim'):
    """
    Plot the histrograms of the sources detcted in the image and by Pan-STARRS
    in the FoV.

    Parameters
    ----------
    region : Astropy table
        Table of the sources detected in the FoV by Pan-STARRS.
    detected_objects : Astropy Table
        Table of the sources detected in the image.
    mag_lim : numpy histogram
        Limit magnitude of the image.
    lim : float
        Value of the limit magnitude of the image.
    band : string
        Filter used to acquire the image.
    precision : float, optional
        Bin size. The default is 0.2.
    threshold : float, optional
        Threshold of the ratio to define where the limit magnitude is reach.
        The default is 0.5.
    name : string, optional
        name for the plot save. The default is 'mag_lim'.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    label = 'Limit Magnitude = {:.1f} $\pm$ {} mag'.format(lim, precision)
    magmax,  magmin = np.max(region[band]), np.min(region[band])
    rg=(magmin, magmax)
    nbin = int((magmax - magmin)/precision)
    ax.axvline(lim, label = label,
               color='grey', linestyle='dashed', linewidth=3)
    ax.hist(detected_objects[band], bins=nbin, alpha=0.5,
            range=rg, label=r'image')
    ax.hist(region[band], bins= nbin, alpha=0.5,
            range=rg, label=r'Pan-STARRS')
    ax.legend()
    ax.set_title(r'Limit Magnitude')
    ax.set_xlabel(r'Magnitude [mag]')
    ax.set_ylabel(r'Number of detected objects')
    # label = r'Limit Magnitude = ' + '%.2f' %lim
    ax.axvline(lim, label = label,color='grey', linestyle='dashed', linewidth=3)
    
    if name is not None:
        fig.savefig(name + '.png')
        plt.close(fig)
    
def do_plot_ratio(mag_lim, lim, region, index, threshold=0.5, precision = 0.2,
                  name='ratio', title=r'Limit Magnitude Ratio'):
    """
    Plot the ratio histogram.

    Parameters
    ----------
    mag_lim : numpy histogram
        Limit magnitude of the image.
    lim : float
        Value of the limit magnitude.
    region : Astropy table
        Table of the sources detected in the FoV by Pan-STARRS.
    index : int
        Index of the histogram where the limit magnitude is reached.
    threshold : float, optional
        Threshold of the ratio to define where the limit magnitude is reach.
        The default is 0.5.
    name : string, optional
        name for the plot save. The default is 'ratio'.
    title : string, optional
        Title of the plot. The default is r'$Limit$ $Magnitude$ $Ratio$'.

    Returns
    -------
    None.

    """
    mask = (mag_lim[:index+1]==0.)
    y = np.ma.array(mag_lim[:index+1], mask=mask).compressed()
    x = np.ma.array(region[1][:index+1], mask=mask).compressed()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    label = 'Limit Magnitude = {:.1f} $\pm$ {} mag'.format(lim, precision)
    ax.axvline(lim, label = label, color='grey',
               linestyle='dashed', linewidth=3)
    ax.plot(x, y, linestyle='none', marker = 'o', color='blue', ms=8)
    ax.plot(region[1][index+1:-1], mag_lim[index+1:], 
            linestyle='none', marker = 'o', color='blue', ms=8)
    ax.axhline(threshold, label = r'threshold', color='black',
               linestyle='-', linewidth=3)
    ax.set_title(title)
    ax.title.set_size(20)
    ax.set_xlabel(r'Magnitude [mag]')
    ax.set_ylabel(r'ratio of detected objects')
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    ax.grid(b=True, which='major', color='#666666', linestyle='-')
    ax.minorticks_on()
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.5)
    ax.legend(prop={"size":15})
    if name is not None:
        fig.savefig(name + '.png')
        plt.close(fig)

def get_mag_lim(mag_lim, detected_objects, precision=0.2, threshold=0.5):
    """
    Get the limit magnitude of the image.

    Parameters
    ----------
    mag_lim : numpy histogram
        Limit magnitude of the image.
    detected_objects : Astropy Table
        Table of the sources detected in the image.
    precision : float, optional
        Bin size. The default is 0.2.
    threshold : float, optional
        Threshold of the ratio to define where the limit magnitude is reach.
        The default is 0.5.

    Returns
    -------
    lim : float
        Value of the limit Magnitude.
    idx : int
        Index of the histogram where the limit magnitude is reached.

    """
    index=0
    # threshold=0.5
    mask=mag_lim>0.
    for i in range(len(mag_lim[mask])):
        sup = mag_lim[mask][i:]>threshold
        if sup.any():
            index+= 1
        else:
            break
    value = mag_lim[mask][index-1]
    idx = np.max(np.where(mag_lim==value))
    lim = round(detected_objects[1][idx].astype('float16') + 0.5 * precision, 2)

    return lim, idx


def compute_mag_lim(data, wcs, band, mu_conf, precision, interval, threshold,
                    path_ratio, path_histo):
    """
    Main function to compute the limit magnitude and plot the ratio.

    Parameters
    ----------
    data : numpy array
        images array.
    wcs : astropy WCS
        Astrometry information.
    band : str
        Filter used to acquire the image.
    mu_conf : dict
        muphoten configuration.
    precision : float
        bin size.
    interval : list
        interval where to find the limit magnitude.
    threshold : float, optional
        Threshold of the ratio to define where the limit magnitude is reach.
    path_ratio : string
        Where to save the plot.

    Returns
    -------
    lim : TYPE
        DESCRIPTION.
    precision : TYPE
        DESCRIPTION.

    """
    width, height = get_fov(data, wcs)
    region = get_region(data, wcs, band)
    all_star_detected = detect_objects(data, wcs, band, mu_conf)
    detected_objects, hist_region, mag_lim = build_ratio(region,
                                                    all_star_detected,
                                                    band,
                                                    precision=precision,
                                                    interval=interval)
    lim, index = get_mag_lim(mag_lim, hist_region,
                             precision=precision,
                             threshold=threshold)
    do_plot_ratio(mag_lim,
                  lim,
                  hist_region,
                  index,
                  threshold,
                  precision,
                  name=path_ratio)

    do_plot_histo(region,
                  all_star_detected,
                  mag_lim,
                  lim,
                  band,
                  name=path_histo)

    return lim, precision
