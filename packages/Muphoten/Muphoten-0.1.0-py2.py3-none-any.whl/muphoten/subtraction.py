#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import hjson
import numpy as np
from astropy.io import fits
from astropy import wcs
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u
from muphoten.registration import registration
from muphoten.ps1_survey import ps1_grid, prepare_PS1_sub
from muphoten.utils import (mkdir_p, rm_p, get_corner_coords)
from muphoten.psfex import psfex
from muphoten.mosaic import create_mosaic
from muphoten.catalog import get_filter
from multiprocessing import Pool


def subtraction(filenames, reference, config, soft="hotpants",
                 method="individual", doMosaic=False, 
                 verbose="NORMAL", outLevel=1, nb_threads=8):
    """Substract a reference image to the input image"""

    imagelist = np.atleast_1d(filenames)
    for ima in imagelist:
        # Create folder with substraction results
        path, filename = os.path.split(ima)
        if path:
            folder = path + "/"
        else:
            folder = ""

        resultDir = folder + "subtraction/"
        # mkdir_p(resultDir)

        # Get coordinates of input image
        im_coords = get_corner_coords(ima)
        print(im_coords)
        hdu = fits.open(ima)[0]
        header = hdu.header

        # Define the reference image
        if reference == "ps1":
            band = get_filter(header)
            if band in ["BMag", "VMag", "cmag", "gmag"]:
                band = "g"
            # elif band == "VMag":
            #     band = "g"
            elif band in ["RMag", "rmag"]:
                band = "r"
            elif band in ["IMag", "imag"]:
                band = "i"
            # elif band == "cmag":
            #     band = "g"
            # band = 'g'
            ps1_cell_table = ps1_grid(im_coords)
            #  Get PS1 files with whom to perform substraction
            subfiles = prepare_PS1_sub(
                ps1_cell_table, band, ima, config, verbose=verbose,
                method=method
            )
            regis_info = registration(
                subfiles, config, resultDir=resultDir, reference=reference,
                verbose=verbose
            )

            if soft == "hotpants":
                subFiles = hotpants(regis_info, config, verbose=verbose,
                                    nb_threads=nb_threads)

            #  create a mosaic of all substracted images when
            # ps1_method=='individual'
            #  Mosaic for substracted files
            if method == "individual" and doMosaic:
                subfiles = np.array(subFiles)
                #  Mosaic for input file
                sublist = [i for i in subfiles[:, 0]]
                outName = os.path.splitext(filename)[0] + "_mosaic"
                create_mosaic(
                    sublist, ima, resultDir, outName, config=config,
                    verbose=verbose
                )
                #  Mosaic for ps1 reference files
                sublist = [i for i in subfiles[:, 1]]
                outName = os.path.splitext(filename)[0] + "_mosaic_ps1"
                create_mosaic(
                    sublist, ima, resultDir, outName, config=config,
                    verbose=verbose
                )
                #  Mosaic for substracted files
                sublist = [i for i in subfiles[:, 2]]
                outName = os.path.splitext(filename)[0] + "_mosaic_sub"
                create_mosaic(
                    sublist, ima, resultDir, outName, config=config,
                    verbose=verbose
                )
                #  Mosaic for mask applied to substracted files
                # Actually there is no need
                
                sublist = [i for i in subfiles[:, 3]]
                outName = os.path.splitext(filename)[0] + "_mosaic_sub_mask"
                create_mosaic(
                    sublist, ima, resultDir, outName, config=config,
                    verbose=verbose
                )

        else:
            subfiles = [[ima, reference, None]]
            regis_info = registration(subfiles, config, resultDir=resultDir)
            subFiles = hotpants(regis_info, config, verbose=verbose,
                                  nb_threads=nb_threads)

    return subFiles


def run_hotpants(hotpants_cmd, hotpants_cmd_file, resmask):
    """Command to execute hotpants. Useful for multiprocessing"""

    os.system("echo %s > %s" % (hotpants_cmd, hotpants_cmd_file))

    os.system(hotpants_cmd)
    
    # Set bad pixel values to 0 and others to 1 for sextractor
    hdulist = fits.open(resmask)
    hdulist[0].data[hdulist[0].data == 0] = 1
    hdulist[0].data[hdulist[0].data != 1] = 0
    hdulist.writeto(resmask, overwrite=True)


def hotpants(regis_info, config, verbose="QUIET", nb_threads=8):
    """Image substraction using hotpants"""

    subfiles = []

    #  Loop over the files
    args = []
    for info in regis_info:
        inim = info["inim"]
        refim = info["refim"]
        maskim = info["mask"]

        path, filename = os.path.split(inim)
        if path:
            folder = path + "/"
        else:
            folder = ""

        resfile = os.path.splitext(inim)[0] + "_sub.fits"
        resmask = os.path.splitext(inim)[0] + "_sub_mask.fits"

        subfiles.append([inim, refim, resfile, resmask])
      
        hotpants_cmd = get_hotpants_cmd(
            inim, refim, maskim, resfile, resmask, info, config, verbose,
            run=1
        )
        hotpants_cmd_file = path + os.path.splitext(filename)[0] + "_hotpants.sh"
        args.append([hotpants_cmd, hotpants_cmd_file, resmask])

    p = Pool(nb_threads)
    p.starmap(run_hotpants, args)
    p.close()
    
    """
        #  Check that substraction performed relatively well
        header = fits.getheader(resfile)
        try:
            X2NRM00 = float(header["X2NRM00"])
            if X2NRM00 > 1:
                flag_bad = True
            else:
                flag_bad = False
        except BaseException:
            flag_bad = True

        flag_bad = False

        if flag_bad:
            print("bad substraction")
            #  try again increasing the sigma of third polynomial for the
            # kernel
            hotpants_cmd = get_hotpants_cmd(
                inim, refim, maskim, resfile, resmask, info, config, verbose,
                run=1
            )

            hotpants_cmd_file = path + os.path.splitext(filename)[0] + "_hotpants.sh"
            os.system("echo %s > %s" % (hotpants_cmd, hotpants_cmd_file))
            os.system(hotpants_cmd)
            header = fits.getheader(resfile)
            try:
                X2NRM00 = float(header["X2NRM00"])
                if X2NRM00 > 1:
                    flag_bad = True
                else:
                    flag_bad = False
            except BaseException:
                flag_bad = True

            if flag_bad:
                print("bad substraction")
                #  Try to increase number of stamps
                hotpants_cmd = get_hotpants_cmd(
                    inim, refim, maskim, resfile, resmask, info, config,
                    verbose, run=1
                )

                hotpants_cmd_file = path + \
                    os.path.splitext(filename)[0] + "_hotpants.sh"
                os.system("echo %s > %s" % (hotpants_cmd, hotpants_cmd_file))
                os.system(hotpants_cmd)
        """


    return subfiles


def get_hotpants_cmd(inim, refim, maskim, resfile, resmask, info,
                     config, verbose, run=1):
    """ Create the hotpants command"""
    if verbose == "QUIET":
        verbosity = 0
    elif verbose == "NORMAL":
        verbosity = 1
    elif verbose == "FULL":
        verbosity = 2

    path, filename = os.path.split(inim)
    if path:
        folder = path + "/"
    else:
        folder = ""

    resfile = os.path.splitext(inim)[0] + "_sub.fits"
    resmask = os.path.splitext(inim)[0] + "_sub_mask.fits"

    if run == 1:
        fname = config["hotpants"]["conf"]
    elif run == 2:
        fname = config["hotpants"]["conf2"]
    elif run == 3:
        fname = config["hotpants"]["conf3"]

    with open(fname) as json_file:
        hotpants_conf = hjson.load(json_file)

    if (
        hotpants_conf["ng"] == "auto"
        or hotpants_conf["r"] == "auto"
        or hotpants_conf["rss"] == "auto"
    ):
        #  Compute PSF FWHM on input and ref images
        FWHM_inim = psfex(inim, config, verbose="QUIET")
        FWHM_refim = psfex(refim, config, verbose="QUIET")

    if hotpants_conf["ng"] == "auto":
        #  transfrom to sigma
        sigma_inim = FWHM_inim[0] / (2 * np.sqrt(2 * np.log(2)))
        sigma_refim = FWHM_refim[0] / (2 * np.sqrt(2 * np.log(2)))
        #  As decribed here https://github.com/acbecker/hotpants
        kernel_match = np.sqrt(sigma_inim ** 2 - sigma_refim ** 2)
        kernel_file = path + os.path.splitext(filename)[0] + "_kernel.dat"
        kernel_txt = "Sigma_ima: %.3f   Sigma_PS1: %.3f    Sigma_kernel: %.3f" % (
            sigma_inim,
            sigma_refim,
            kernel_match,
        )
        os.system("echo %s > %s" % (kernel_txt, kernel_file))
        #  update config file for hotpants
        hotpants_conf["ng"] = "3 6 %.2f 4 %.2f 2 %.2f" % (
            0.5 * kernel_match,
            kernel_match,
            2 * kernel_match,
        )

    if hotpants_conf["r"] == "auto":
        #  seeing*2.5  DECAM, arbitray
        #  seeing*2.5 here: https://arxiv.org/pdf/1608.01006.pdf
        hotpants_conf["r"] = str(int(FWHM_inim[0] * 2.35 * 2.5))
    if hotpants_conf["rss"] == "auto":
        # DECAM: seeing*5
        #  seeing*6 here: https://arxiv.org/pdf/1608.01006.pdf
        hotpants_conf["rss"] = str(int(FWHM_inim[0] * 2.5 * 5))

    # Set min and max acceptable values for input and template images
    # Too simple, need to adapt it in the future
    il = str(info["in_lo"])
    iu = str(info["in_up"])
    tl = str(info["ref_lo"])
    tu = str(info["ref_up"])
    overlap = "%s, %s, %s, %s" % (
        info["XY_lim"][0],
        info["XY_lim"][1],
        info["XY_lim"][2],
        info["XY_lim"][3],
    )

    hotpants_cmd = "hotpants -inim %s -tmplim %s -outim %s -omi %s " % (
        inim,
        refim,
        resfile,
        resmask,
    )
    # hotpants_cmd += '-il %s -iu %s -tl %s -tu %s -gd %s ' % (il, iu, tl,
    #                                                           tu, overlap)
    hotpants_cmd += "-il %s -iu %s -tl %s -tu %s " % (il, iu, tl, tu)
    hotpants_cmd += "-tuk %s -iuk %s " % (tu, iu)
    hotpants_cmd += "-ig %s -tg %s " % (info["gain_in"], info["gain_ref"])
    hotpants_cmd += "-v %s " % verbosity

    if maskim:
        hotpants_cmd += "-tmi %s " % maskim

    # Add params from the hjson conf file
    for key, value in hotpants_conf.items():
        hotpants_cmd += "-%s %s " % (key, value)

    return hotpants_cmd
