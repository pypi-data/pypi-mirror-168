#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 20:08:31 2020.

@author: duverne
"""

from astropy.visualization import ZScaleInterval, imshow_norm, SqrtStretch
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
import numpy as np
from astropy.table import Table
from astropy.stats import sigma_clip

def plot_image(data, sky_ap=None, ap=None, wcs=None, path2save=None,
               name='/apertures.png'):
    """
    Display the image.

    Parameters
    ----------
    data : image array

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 12.5))
    imshow_norm(data, ax,  origin='lower', cmap = 'Greys_r',
                interval=ZScaleInterval(), stretch=SqrtStretch())
    ax.set_xlabel(r'X')
    ax.set_ylabel(r'Y')
    ax.set_title(r'Apertures')
    if ap is not None:
        for aperture in ap:
            aperture.plot(axes=ax, color='red', lw=1.5)
    if sky_ap is not None:
        for aperture in sky_ap:
            aperture.to_pixel(wcs).plot(axes=ax, color='red', lw=1.5)
    if path2save is not None:
        fig.savefig(path2save + name)
        plt.close(fig)

def plot_sementation_image(segmentation, path2save=None):
    """
    Display segmentation image.

    Parameters
    ----------
    segmentation : photutils segmentation objet

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 12.5))
    cmap = segmentation.make_cmap(seed=123)
    ax.imshow(segmentation, origin='lower',
              cmap=cmap)
    ax.set_xlabel(r'X')
    ax.set_ylabel(r'Y')
    ax.set_title(r'Segmentation Map')
    if path2save is not None:
        fig.savefig(path2save + '/segmentation.png')
        plt.close(fig)

def plot_background(data, background, dif=False, save=False, path=None):
    """
    Display backgroung image or the result of the background subtraction.

    Parameters
    ----------
    data : image array
    background : background array
    dif : boolean, optional
        wether or not display the result of the background subtraction.
        The default is False.
    save : boolean, optional
        Save the figure.
    path : str, optional
        Path where the figure is saved.

    Returns
    -------
    None.

    """
    if dif:
        fig, ax = plt.subplots(1, 3, figsize=(10, 12.5))
        imshow_norm(data, ax[0],  origin='lower', cmap = 'Greys_r',
                    interval=ZScaleInterval(), stretch=SqrtStretch())
        imshow_norm(background, ax[1],  origin='lower', cmap = 'Greys_r',
                    interval=ZScaleInterval(), stretch=SqrtStretch())
        imshow_norm(data-background, ax[2],  origin='lower', cmap = 'Greys_r',
                    interval=ZScaleInterval(), stretch=SqrtStretch())
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12.5, 12.5))
        im, norm = imshow_norm(background, ax,  origin='lower', cmap = 'Greys_r',
                    interval=ZScaleInterval(), stretch=SqrtStretch())
        ax.set_xlabel(r'$X$')
        ax.set_ylabel(r'$Y$')
        ax.set_title(r'$Background$ $Map$')
        fig.colorbar(im, ax=ax)
        if save:
            try:
                fig.savefig(path)
                plt.close(fig)
            except ValueError:
                raise ValueError("Need a path where to save the plot.")

def plot_calib(band, source, fit_coef, da_2, db_2, path2save=None):
    """
    Plot the calibration curve for an image

    Parameters
    ----------
    band : str
        Filter used to acquire the image.
    source : astropy Table
        Table contatining the calibration informations.
    fit_coef : numpy array, list
        Fit parameters of the calibration.
    path2save : str, optional
        Where to save the figure created if a path is given.
        The default is None.

    Returns
    -------
    None.

    """

    fig, ax = plt.subplots(1, 1, figsize=(12.5, 12.5))

    fit_lin = poly.polyval(source['Magnitude'],
                           np.flip(fit_coef))
    source['mag_err'] = 2.5/(np.log(10)*np.sqrt(source['aperture_sum']))
    da, db = np.sqrt(da_2), np.sqrt(db_2) 
    ax.plot(source['Magnitude'],
            fit_lin,
            label = r'Fit : a={0:.2f} $\pm$ {1:.2f} and zp={2:.2f} $\pm$ {3:.2f}'.format(fit_coef[0], da, 
                                                                                         fit_coef[1], db),
            color='red')
    khi = np.sum(((fit_lin - source[band]) ** 2)/source['error'])
    khi_dof = khi/(len(source['Magnitude']) - 2)
    label = r'$\frac{\chi^2}{dof}$'
    label+= r' = {0:.3f}'.format(khi_dof)
    ax.errorbar(source['Magnitude'], 
                source[band],
                xerr=source['mag_err'],
                yerr=source['error'],
                marker="x",
                ms='9',
                color='black' ,
                linestyle='none',
                label = label)
    ax.set_xlabel(r'Instrumental Magnitude [mag]', fontsize=18)
    ax.set_ylabel(r'Catalog Magnitude [mag]', fontsize=18)
    ax.set_title(r'Calibration Curve', fontsize=18)
    
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    ax.grid(visible=True, which='major', color='#666666', linestyle='-')
    ax.minorticks_on()
    
    ax.legend(fontsize=18)
    if path2save is not None:
        fig.savefig(path2save + '/calibration.png')
        plt.close(fig)

def add_error(data_table):

    data_table['err_bkg'] = 2.5/(np.log(10)*np.sqrt(np.abs(data_table['bkg_sum'])))
    data_table['err_bkg_sub'] = 2.5/(np.log(10)*np.sqrt(np.abs(data_table['background_sum'])))
    data_table['err_tot'] = np.sqrt(data_table['err_bkg']**2
                                    + data_table['error']**2
                                    + data_table['err_bkg_sub']**2)
    data_table['star_ref_err_bkg_sub'] = 2.5/(np.log(10)*np.sqrt(np.abs(data_table['star_ref_bkg_sum'])))
    data_table['star_ref_err_tot'] = np.sqrt(data_table['star_ref_error']**2
                                             + data_table['star_ref_err_bkg_sub']**2)
    
    return data_table
    

def is_mag_comptible(data_table):
    
    data_table['star_ref_magnitude_inf'] = (data_table['star_ref_magnitude'] 
                                            - data_table['star_ref_error_tot'])
    data_table['star_ref_magnitude_sup'] = (data_table['star_ref_magnitude'] 
                                            + data_table['star_ref_error_tot'])
    
    data_table['star_ref_magnitude_cata_inf'] = (data_table['star_ref_magnitude_cata'] 
                                                 - data_table['star_ref_error_cata'])
    data_table['star_ref_magnitude_cata_sup'] = (data_table['star_ref_magnitude_cata'] 
                                                 + data_table['star_ref_error_cata'])

    mask1 = (data_table['star_ref_magnitude_sup'] > data_table['star_ref_magnitude_cata_inf'])
    data_table = data_table[mask1]
    mask2 = (data_table['star_ref_magnitude_inf'] < data_table['star_ref_magnitude_cata_sup'])
    data_table = data_table[mask2]

    return data_table

def prepare_light_curve(data_file, clipping_psf=3., err_star=1.0, tele='undef' ):
    
    data_table = Table.read(data_file,
                            format='ascii.commented_header')
    
    bkg_time = np.mean(data_table['time_bkg'])
    photo_time = np.mean(data_table['time_phot_time'])
    xmatch_time = np.mean(data_table['time_xmatch'])
    sub_time = np.mean(data_table['time_sub'])
    im_time = np.mean(data_table['time_image'])
    
    n_im = len(data_table)
    print('{} images processed for {}'.format(len(data_table), tele))
    mask = (data_table['flag_dist'] == 0)
    data_table = data_table[mask]
    print('{} images with detection for {}'.format(len(data_table), tele))
    print('{} images without detection for {}'.format(n_im - len(data_table),
                                                      tele))
    n_im = len(data_table)
    mask = (data_table['star_ref_error_tot'] < err_star)
    data_table = data_table[mask]
    data_table = is_mag_comptible(data_table)
    print('{} images passed star veto for {}'.format(len(data_table), tele))
    print('{} images rejected by star veto'.format(n_im - len(data_table)))
    n_im = len(data_table)
    clip = sigma_clip(data_table['psf'], sigma = clipping_psf, masked=True)
    clip_mask = np.invert(clip.recordmask)
    data_table = data_table[clip_mask]
    print('{} images passed PSF veto for {}'.format(len(data_table), tele))
    print('{} images rejected by PSF veto'.format(n_im - len(data_table)))
    print('{} valid images'.format(len(data_table)))
    
    print('Mean poisson error {} for {}'.format(np.mean(data_table['error']),
                                                tele))
    print('Mean calibration error {} for {}'.format(np.mean(data_table['error_calib']),
                                                    tele))
    print('Mean background error {} for {}'.format(np.mean(data_table['error_bkg']),
                                                   tele))
    
    print('Mean time processing bkg : {} for {}'.format(bkg_time, tele))
    print('Mean time processing photo : {} for {}'.format(photo_time, tele))
    print('Mean time processing xmatch : {} for {}'.format(xmatch_time, tele))
    print('Mean time processing sub image : {} for {}'.format(sub_time, tele))
    print('Mean time processing one image : {} for {}'.format(im_time, tele))
    print('Total time processing {} for : {}'.format(data_table['tot_time'][0],
                                                     tele))

    return data_table

def plot_star_ref(file, telescope, band, clipping_psf=3.0,
                  err_star=1.0, xlabel=r'$Time$', save=False, display=True):
    
    # plot lc star ref #   
    fig, main_axes = plt.subplots(1,1)
    plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1,
                              right = 0.9, top = 0.9,
                              wspace = 2.5, hspace = 0.5)
    
    ##### resultats TCH - bande g #####
    cleaned = prepare_light_curve(file, clipping_psf, err_star)

    ###### for raw plots ####
    raw = Table.read(file, format='ascii.commented_header')
    mask = (raw['flag_dist'] == 0)
    raw = raw[mask]
    
    ### Cleaned plots ###
    main_axes.errorbar(raw['time'],
                        raw['star_ref_magnitude'],
                        yerr=raw['star_ref_error_tot'],
                        label= band + ' ' + r'band' + ' ' + telescope +
                        ' '+'raw',
                        marker = 'x', linestyle = 'none',
                        color = 'red', ms=5)
    main_axes.errorbar(cleaned['time'],
                        cleaned['star_ref_magnitude'],
                        yerr=cleaned['star_ref_error_tot'],
                        label= band + ' ' + r'$band$' + ' ' + telescope,
                        marker = 'd', linestyle = 'none',
                        color = 'blue', ms=7)
    main_axes.errorbar(raw['time'],
                        raw['star_ref_magnitude_cata'],
                        yerr=raw['star_ref_error_cata'],
                        label= r'$Catalog$ $Magnitude = $'+ '%.2f' %raw['star_ref_magnitude_cata'][0],
                        linestyle = '-',
                        color = 'black', ms=5)
    

    main_axes.set_xlabel(xlabel)
    main_axes.set_ylabel(r'$Magnitude$')
    main_axes.set_title(r'$Lightcurve$ $Star$' + ' ' + telescope)
    main_axes.legend()
    main_axes.invert_yaxis()
    if save:
        fig.savefig(band+'star_ref_' + telescope + '.png')
        plt.close(fig)
    if not display:
        plt.close(fig)
    