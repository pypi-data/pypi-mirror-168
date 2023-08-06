#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 16:58:12 2021

@author: duverne, IJClab, Orsay, duverne@protonmail.com
"""

import argparse, os, glob, sys, hjson, warnings
# import time
from astropy.io import fits
from astropy.wcs import WCS, FITSFixedWarning
from astropy import units as u
import numpy as np
import numpy.polynomial.polynomial as pl

from muphoten.background import sub_background
from muphoten.utils import (load_coord_file,
                            getTel, make_results_dir, get_filename,
                            list_files, load_config, set_results_table,
                            make_sub_result_rep, PhotList)
from muphoten.sanitise import sanitise_fits
from muphoten.catalog import (get_filter, getCata, CataList, calibration,
                              catalog_choice, )
from muphoten.photometry import (source_detection, Kron_Photometry, masking,
                                 Fixed_Photometry, Isophotal_Photometry,
                                 Dophot, get_source, compute_error,
                                 compute_snr)
from muphoten.psfex import psfex
from muphoten.plot_image import (plot_sementation_image,
                                 plot_image, plot_calib)

warnings.filterwarnings("ignore", category=FITSFixedWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

"""Muphoten main script for photometry."""

def main():
    """Console script for muphoten."""
    # path_muphoten = getpath()
    telescope_list = getTel()
    catalog_list = CataList()
    phot_list = PhotList()
    parser = argparse.ArgumentParser(description="Performing photometry of\
                                     transient objects.")

    parser.add_argument("--coord",
                        dest="coord",
                        required=True,
                        type=str,
                        help="Coordinates file's path.")

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
                        required=True,
                        type=str,
                        help="Telescope that acquired the images.")

    parser.add_argument("--catalog",
                        dest="catalog",
                        choices=catalog_list,
                        required=False,
                        type=str,
                        help="Catalog to use for the calibration.")

    parser.add_argument("--photo",
                        dest="photo",
                        default='iso',
                        choices=phot_list,
                        help="Type of photometry. Use muphoten configuration \
                              file to modify the radius of the isophote or the \
                              factor used for the fixed apertures.\
                              Default is iso.")

    parser.add_argument("--sub-method",
                        default='sub',
                        choices=['sub', 'nosub'], # , 'nosub'],
                        help="Wether HOTPANTS has been used to perform"
                             "template subtraction (sub) or not (nosub).")

    parser.add_argument("--keep-old",
                        "--keep",
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

    parser.add_argument("--band",
                        required=False,
                        choices=['UMag', 'BMag', 'VMag', 'RMag', 'IMag',
                               'umag', 'gmag', 'rmag', 'imag', 'zmag',
                               'cmag'],
                        help="Band used to acquire the image. To use if the"
                             "'FILTER' keyword is not in the fits header."
                             "Use Capital name for Johson-Cousins filters,"
                             "use lowercase names for the Sloan filters,"
                             "use cmag name for unfiltered images and "
                             "luminance filter.")

    parser.add_argument("--mask-size",
                        dest="mask",
                        required=False,
                        type=int,
                        help="Using a square mask centered on the transient."
                             "Beyond this mask, the source are"
                             "not used for the calibration. ")

    parser.add_argument("--save-bkg",
                        dest="save_bkg",
                        action="store_true",
                        help="Save the background images as fits and png.\
                              Default : False")

    args = parser.parse_args()

    # Loading the coordinates of the analysed objects
    sources, stars = load_coord_file(args.coord)
    print('Computing lightcurve for {} sources'.format(len(sources)))
    print('Using {} stars to veto poor quality images'.format(len(stars)))

    print('Loading configuration for Muphoten,')
    config = load_config(args.telescope)
    mu = config['muphoten']['conf']
    with open(mu) as json_file:
        mu_conf = hjson.load(json_file)

    # Preparing the files for analysis
    images = list_files(args.images, get_subdirs=False)
    print('{} images to calibrate'.format(len(images)))
    # glob_start = time.time()
    results_file = os.path.join(args.images, 'results')
    col_name = ['filename',
                'telescope',
                'filter',
                'time',
                'psf',
                'a', 'da',
                'b', 'db',
                'src_centroid_ra',
                'src_centroid_dec',
                'src_flux',
                'src_bkg_flux',
                'src_ins_mag',
                'src_mag',
                'src_SNR',
                'src_bkg_err',
                'src_flux_err',
                'src_calib_err',
                'src_tot_err',
                'src_det',
                'ref_mag',
                'ref_mag_cata',
                'ref_tot_err',
                'ref_cata_err',
                'ref_flux',
                'ref_bkg_flux',
                'ref_SNR',
                'ref_dist']
    res = set_results_table(col_name, len(images))

    for i, image in enumerate(images):
        image = make_results_dir(image,
                                 directory='calibration',
                                 keep=args.keep,
                                 skip=args.skip)
        image_name = get_filename(image)
        res['filename'][i] = image_name
        image_rep = os.path.dirname(image)
        calib_rep = os.path.join(image_rep, 'calibration')
        print(calib_rep)
        sub_rep = os.path.join(image_rep, 'subtraction/')
        print(sub_rep)
        # start_im_time = time.time()  # Computing time for one image processing
        print('Processing image n° {} : {}'.format(i, image_name))
        print('Sanitising header')
        sanitise_fits(image)
        print(image)
        # Load the data
        hdu = fits.open(image)[0]
        data, header = hdu.data, hdu.header
        wcs_data = WCS(header)
        if 'TELESCOP' in header.keys():
            res['telescope'][i] = header['TELESCOP']
        else:
            res['telescope'][i] = args.telescope
        exp_time = float(header['EXPTIME'])

        # Getting different useful informations : band, MJD,
        # catalog for calibration.
        res['time'][i] = header.get('MJD-OBS')
        if args.catalog:
            catalog, system = getCata(args.catalog)
            cata_name = args.catalog
        else:
            catalog, system, cata_name = catalog_choice(header)

        if args.band:
            band = args.band
        else:
            band = get_filter(header)

        res['filter'][i] = band
        
        print('Subtracting background in image : {}'.format(image_name))
        # Getting the backgroud, rms and bkg subtracted images
        if args.save_bkg:
            make_sub_result_rep(image_rep, directory='background')
            path2save = image_rep
        else:
            path2save = None
        data_clean, background,\
            rms = sub_background(data, header,
                                 image_name,
                                 n_sigma=mu_conf['bkg_n_sigma'],
                                 box_size=mu_conf['bkg_box'],
                                 bkg_estimator=mu_conf['bkg_estimator'],
                                 filter_size=mu_conf['bkg_filter_size'],
                                 path2save=path2save,
                                 png=args.save_bkg)

        # Detection of the sources & segmentation
        mask=None
        if args.mask:
            mask = masking(data_clean, sources, header, args.mask)
        segmentation = source_detection(data, background, rms,
                                        n_sigma=mu_conf['det_n_sigma'],
                                        deblend=mu_conf['det_deblend'],
                                        mask=mask,
                                        threshold_level=mu_conf['det_treshold'],
                                        npixels=mu_conf['det_npixels'],
                                        contrast=mu_conf['contrast'])
        plot_sementation_image(segmentation, path2save=calib_rep)
        # Computing PSF
        print('Computing PSF for image n° {}'.format(i))
        make_sub_result_rep(image_rep, directory='psf')
        FWHM_psf = psfex(image, config, verbose="QUIET")
        res['psf'][i] = FWHM_psf[0]
        print(FWHM_psf[0])
        if args.photo == phot_list[0]:  # Kron photometry
            print('Performing Kron Photometry')
            photometry_table = Kron_Photometry(data, data_clean, segmentation,
                                               header, background, rms,
                                               wcs=wcs_data)
            plot_image(data_clean, ap=photometry_table['kron_aperture'],
                       wcs=wcs_data, path2save=calib_rep)
        if args.photo == phot_list[1]:
            print('Performing Isophotal Photometry')
            photometry_table = Isophotal_Photometry(data, data_clean,
                                                    segmentation, header,
                                                    background, rms,
                                                    radius=mu_conf['radius_iso'],
                                                    wcs=wcs_data)
            plot_image(data_clean, sky_ap=photometry_table['aperture'],
                       wcs=wcs_data, path2save=calib_rep)
        if args.photo == phot_list[2]:
            print('Performing Fixed size Photometry')
            radius = mu_conf['fixed_factor'] * FWHM_psf[0]
            photometry_table = Fixed_Photometry(data, data_clean, segmentation,
                                                header, radius, background,
                                                rms, wcs=wcs_data)
            plot_image(data_clean, sky_ap=photometry_table['aperture'],
                       wcs=wcs_data, path2save=calib_rep)

        if args.sub_method == 'nosub': # no template subtraction performed
            src = get_source(photometry_table, sources, wcs_data)
            dist = src['dist'][0]

        print('Performing calibration using {}'.format(cata_name))
        photometry_table, coefs,\
            da_2, db_2, star_ref = calibration(source=photometry_table,
                                               catalog=catalog,
                                               cata_phot_syst=system,
                                               stars=stars,
                                               wcs_data=wcs_data,
                                               n_sigma=mu_conf['clipping_calib'],
                                               cut_mag=mu_conf['cut_mag'],
                                               band=band)
        plot_calib(band, photometry_table,
                   coefs, da_2, db_2,
                   path2save=calib_rep)
        photometry_table.write(calib_rep + '/calibration.dat',
                               format='ascii.commented_header',
                               overwrite=True)

        # Saving the calibration results.
        res['a'][i] = coefs[0]
        res['da'][i] = np.sqrt(da_2)
        res['b'][i] = coefs[1]
        res['db'][i] = np.sqrt(db_2)

        # Saving the results for the reference star.
        star_ref = compute_error(star_ref, coefs[0], da_2, db_2)
        star_ref = compute_snr(star_ref)
        star_ref = star_ref.filled(0.) # fill the table empty columns with zero
                                       # to avoid issue with masked value.

        res['ref_tot_err'][i] = star_ref['total_error'][0]
        res['ref_mag_cata'][i] = star_ref[band][0]
        res['ref_cata_err'][i] = star_ref['error'][0]
        res['ref_flux'][i] = star_ref['aperture_sum'][0]
        res['ref_mag'][i] = star_ref['Calibrated_Mag'][0]
        res['ref_bkg_flux'][i] = star_ref['background_sum'][0]
        res['ref_SNR'][i] = star_ref['SNR'][0]

        if star_ref['dist'][0] < 5:
            res['ref_dist'][i] = 0  # Reference star detected
        else:
            res['ref_dist'][i] = 1  # Reference star not detected

        if args.sub_method != 'nosub': # no template subtraction performed
            # Detecting the transient in the subtracted image.
            print('Treating subtracted image')
            sub_im = glob.glob(sub_rep + '*.fits')[0]
            print('SUBIMAGE =', sub_im)
            hdu_sub = fits.open(sub_im)[0]
            data_sub, header_sub = hdu_sub.data, hdu_sub.header
            wcs_sub = WCS(header_sub)

            # start_sub_time = time.time()
            mask = (data_sub == 1e-30) | (data_sub == 0)
            data_clean_sub, background_sub,\
                rms_sub = sub_background(data_sub, header_sub,
                                         image_name,
                                         n_sigma=mu_conf['bkg_n_sigma_sub'],
                                         box_size=mu_conf['bkg_box_sub'],
                                         bkg_estimator=mu_conf['bkg_estimator'],
                                         filter_size=mu_conf['bkg_filter_size_sub'],
                                         mask=mask)
            # Creating a mask centered on the transient to avoid the source
            # detection in all the sub image. Otherwise, there could issues
            # because of artefacts due to the subtraction in the sub image.
            mask = masking(data_clean_sub, sources, header_sub, 50)
            seg_sub = source_detection(data_sub,
                                       background_sub,
                                       rms_sub,
                                       n_sigma=mu_conf['det_n_sigma_sub'],
                                       deblend=mu_conf['det_deblend_sub'],
                                       threshold_level=mu_conf['det_treshold_sub'],
                                       npixels=mu_conf['det_npixels_sub'],
                                       contrast=mu_conf['contrast_sub'],
                                       mask=mask)
            # If the transient is not detected in the image
            if seg_sub is None:
                res['src_det'][i] = 1
                print('No transient detected')
                continue
            else:
                if args.photo == phot_list[0]:  # Kron photometry
                    print('Performing Kron Photometry in sub image')
                    photometry_sub = Kron_Photometry(data_sub, data_clean_sub,
                                                     seg_sub,
                                                     header_sub, background_sub,
                                                     rms_sub, wcs=wcs_sub)
                if args.photo == phot_list[1]:
                    print('Performing Isophotal Photometry in sub image')
                    photometry_sub = Isophotal_Photometry(data_sub,
                                                          data_clean_sub,
                                                          seg_sub, header_sub,
                                                          background_sub,
                                                          rms_sub,
                                                          radius=mu_conf['radius_iso'],
                                                          wcs=wcs_sub)

                if args.photo == phot_list[2]:
                    print('Performing Fixed size Photometry in sub image')
                    radius = mu_conf['fixed_factor'] * FWHM_psf[0]
                    photometry_sub = Fixed_Photometry(data_sub,
                                                      data_clean_sub,
                                                      seg_sub,
                                                      header_sub, radius,
                                                      background_sub,
                                                      rms_sub, wcs=wcs_sub)
    
                src = get_source(photometry_sub, sources, wcs_sub)
                print('SOURCE', len(src))
                dist = src['dist'][0]
                if args.photo == phot_list[0]:
                    plot_image(data_clean_sub,
                               ap=src['kron_aperture'],
                               wcs=wcs_sub,
                               path2save=calib_rep,
                               name='/sub_aperture')
                else:
                    plot_image(data_clean_sub,
                               sky_ap=src['aperture'],
                               wcs=wcs_sub, path2save=calib_rep,
                               name='/sub_aperture')
        print('Distance to the source = {}'.format(dist))
        if dist < 15.: # Considering that the transient has been detected
            res['src_det'][i] = 0
            flux = src['aperture_sum'][0]
            if args.sub_method=='sub':
                flux = flux * exp_time

            mag = -2.5*np.log10(flux)
            bkg_sum = Dophot(background, sources, wcs_data,
                             aperture=src['aperture'][0])

        else:
            res['src_det'][i] = 1
            # Computing the number of counts in a 5 pixels circular aperture
            # to have an upper limit on the transient's magnitude.
            if args.sub_method == 'nosub':
                flux = Dophot(data_clean, sources, wcs_data, radius=5.0)
            # elif args.sub_method=='ps':
            #     flux = Dophot(data_sub, sources, wcs_sub, radius=5.0) * exp_time
            else:
                flux = Dophot(data_sub, sources, wcs_sub, radius=5.0) * exp_time
            mag = -2.5*np.log10(flux)
            bkg_sum = Dophot(background, sources, wcs_data, radius=5.0)
        res['src_centroid_ra'][i] = float(src['sky_centroid'].ra / u.deg)
        res['src_centroid_dec'][i] = float(src['sky_centroid'].dec / u.deg)
        res['src_flux'][i] = abs(flux)
        res['src_bkg_flux'][i] = bkg_sum
        res['src_ins_mag'][i] = mag
        res['src_mag'][i] = pl.polyval(mag, np.flip(coefs))
        res['src_SNR'][i] = flux / np.sqrt(flux + bkg_sum)
        res['src_bkg_err'][i] = 2.5 / (np.log(10)*np.sqrt(abs(bkg_sum)))
        res['src_flux_err'][i] = 2.5/(np.log(10)*np.sqrt(flux))
        res['src_calib_err'][i] = np.sqrt(mag**2 * da_2 + db_2 +
                                          coefs[0]*res['src_flux_err'][i]**2)
        res['src_tot_err'][i] = np.sqrt(res['src_flux_err'][i]**2 +
                                            res['src_bkg_err'][i]**2 +
                                            res['src_calib_err'][i]**2)
        print('Transient detected with magnitude {}'.format(res['src_mag'][i]))
        print('Error on the magnitude is {}'.format(res['src_tot_err'][i]))

        # res.show_in_browser(jsviewer=True)
    # res.show_in_browser(jsviewer=True)
    res.write(results_file + '/' + args.outname,
              format='ascii.commented_header',
              overwrite=True)
    return 0


if __name__ == "__main__":
    main()
