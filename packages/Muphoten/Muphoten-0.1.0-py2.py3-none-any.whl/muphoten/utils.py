#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:31:08 2021

@author: duverne & Corre, duverne@protonmail.com
"""
import os, os.path
import errno
import glob
import importlib
import shutil
import time
import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS

def is_subdir(path, basepath):
    """ Checks whether the path is inside basepath """
    path = os.path.abspath(path)
    basepath = os.path.abspath(basepath)

    return os.path.commonpath([path, basepath]) == basepath


def is_psf(filename, patterns=['_psf.fits']):
    """
    Check whether a file is a PSF file with a standard name, typically
    '_psf.fits'. This is used for the simulation of sources during the CNN
    training for instance.
    """
    flag = False
    for ptn in patterns:
        if ptn in filename:
            flag = True
            break

    return flag

def list_files(paths, pattern=["*.fit", "*.fits", "*.fts"],
                recursive=True, get_subdirs=True, exclude=None):
    """ (Recursively) list the files matching the pattern from the list of
    filenames or directories, omitting the ones containing file paths
    specified by 'exclude' option (either string or list of strings)"""

    filenames = []
    subdirs = []

    # Make sure paths is array-like
    paths = np.atleast_1d(paths)

    # Check if paths or files provided by user do exist.
    # filenames or folders can be a list
    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                path
            )

    # If there are than one pth provided keep the exact same structure
    # Otherwise skip the basepath
    for path in paths:
        # List all the files in the given path
        if os.path.isdir(path):
            # Recursively get all files matching given pattern(s)
            filenames_path = []

            for ptn in np.atleast_1d(pattern):
                filenames_path += glob.glob(path + "/**/" +
                                            ptn, recursive=recursive)
            # Sort alphanumerically
            filenames_path.sort()
            filenames += filenames_path
            # Get the relative path folder namesrelative to input paths
            reldirs = [os.path.dirname(os.path.relpath(_, path))
                       for _ in filenames_path]
            # When more than one argument, add the base directory
            # being the last directory name provided by the user.
            if len(paths) > 1:
                basedir = os.path.basename(os.path.abspath(path))
                subdirs += [os.path.join(basedir, _) for _ in reldirs]
            else:
                subdirs += reldirs
        else:
            # if path is not a directory, assume it is a file
            filenames += [path]
            subdirs += ['']

    if isinstance(exclude, str):
        folder2skip = [exclude]
    elif exclude:
        folder2skip = exclude
    else:
        folder2skip = []

    idx = []  # Boolean mask whether to keep the filename or not

    for f in filenames:
        flag_2keep = True
        # If file is a standard PSF fits file
        if is_psf(f, patterns=['_psf.fits', 'SUB',
                               'sub', 'conv',
                               'noisemap', 'clean', 'image',
                               'badpix', 'dupe', 'background',
                               'results', '_ref', 'old', '_veto']):
            flag_2keep = False
        else:
            for text in folder2skip:
                if is_subdir(f, text):
                    flag_2keep = False
                    break

        idx.append(flag_2keep)

    idx = np.array(idx)
    filenames = np.array(filenames)
    subdirs = np.array(subdirs)

    if get_subdirs:
        return filenames[idx], subdirs[idx]
    else:
        return filenames[idx]

def prepare_file(path):

    images = list_files(path, get_subdirs=False)
    prepared_list = []
    for image in images:
        image_name = image.split('/')[-1].split('.')[0]
        im = path + image_name
        sub = glob.glob(im +'/subtraction/*.fit*') # adding subtracted image
        if len(sub) > 0:
            sub = sub[0]
        else:
            sub = ''
        psf = glob.glob(im +'/psf/*.fit*') # adding psf file,
        if len(psf) > 0 : # necessary for vetoing
            psf = psf[0]
        else:
            psf = ''
        back = glob.glob(im +'/background/*.fit*')
        if len(back) > 0:
            back = back[0] # adding background file
            clean = back[1] # adding background subtracted image
        else:
            back = ''
            clean = ''
        prepared_list.append([image, sub, psf, back, clean])

    return prepared_list

def load_coord_file(path):

    coordinates = Table.read(path, format='ascii.commented_header')
    transients = coordinates[coordinates['type']=='transient']
    stars = coordinates[coordinates['type']=='star']
    coord_stars, coord_transients = [], []


    for transient in transients:
        coord_transients.append([transient['Ra'], transient['Dec']])
    if coord_transients[0] == 0:
        raise ValueError('No coordinates found for transient.')

    for star in stars:
        coord_stars.append([star['Ra'], star['Dec']])
        coord_stars[0]
    if len(stars) == 0:
        raise ValueError('No coordinates found for reference star.\
                         Needed to veto poor quality images.')
    return coord_transients, coord_stars

def createFITS(data, header, filename = 'image.fits'):
    hdu = fits.PrimaryHDU(data)
    hdul = fits.HDUList([hdu])
    hdul.writeto(filename, overwrite=True)
    fits.writeto(filename, data, header, overwrite=True,
                 output_verify='ignore')

def load_config(telescope, convFilter='default'):
    """Load the path to the configuration files required by the softs.
       They are telescope dependent.
    """
    path = getpath()
    path2tel = os.path.join(path, "config", telescope)
    config = {
        "telescope": telescope,
        "sextractor": {
            "conf": os.path.join(path2tel, "sourcesdet.sex"),
            "param": os.path.join(path2tel, "sourcesdet.param"),
            "convFilter": os.path.join(
                path,
                "config/conv_kernels/%s.conv" % convFilter
            )
        },
        "scamp": {
            "sextractor": os.path.join(path2tel, "prepscamp.sex"),
            "param": os.path.join(path2tel, "prepscamp.param"),
            "conf": os.path.join(path2tel, "scamp.conf"),
        },
        "swarp": {},
        "psfex": {
            "sextractor": os.path.join(path2tel, "preppsfex.sex"),
            "param": os.path.join(path2tel, "preppsfex.param"),
            "conf": os.path.join(path2tel, "psfex.conf"),
        },
        "hotpants": {
            "conf": os.path.join(path2tel, "hotpants.hjson"),
            "conf2": os.path.join(path2tel, "hotpants_2.hjson"),
            "conf3": os.path.join(path2tel, "hotpants_3.hjson"),
        },
        "muphoten": {
            "conf": os.path.join(path2tel, "muphoten.hjson"),
        },
    }

    return config

def getpath():
    """Get the path to muphoten package"""
    try:
        findspec = importlib.util.find_spec("muphoten")
        path = findspec.submodule_search_locations[0]
    except BaseException:
        print("path to muphoten can not be found.")

    return path

def PhotList():
    return ['kron', 'iso', 'fixed']

def getTel():
    """Get the list of all telescopes"""
    path_muphoten = getpath()
    telList = [name for name in os.listdir(os.path.join(path_muphoten, "config"))
               if os.path.isdir(os.path.join(path_muphoten, "config", name)) and
               name != 'conv_kernels']
    return telList

def cp_p(src, dest):
    try:
        shutil.copy(src, dest)
    except BaseException:
        pass


def mv_p(src, dest):
    try:
        shutil.move(src, dest)
    except BaseException:
        pass


def rm_p(src):
    fileList = glob.glob(src, recursive=False)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except BaseException:
            pass

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_filename(path):
    filename = os.path.splitext(os.path.split(path)[1])[0]
    return filename

def make_results_dir(filename, directory, keep=False, skip=False):
    """ Make the results folder """

    # get name of repertory
    dirname = os.path.dirname(filename)

    results_folder = os.path.join(dirname, 'results')
    if not os.path.exists(results_folder):
        mkdir_p(results_folder)
    dirname = results_folder
    # get filename
    file = os.path.basename(filename)
    # Subdir to store results for this file

    basename = os.path.splitext(file)[0]
    if not basename == os.path.basename(dirname):
        mkdir_p(os.path.join(dirname, basename))
        dirname = os.path.join(dirname, basename)
    # Full path for the file
    newrep = os.path.join(dirname, directory)
    # Make output dir
    if os.path.exists(newrep):
        if skip:
            return None
        elif keep:
            mv_p(newrep, newrep + '_' + time.strftime("%Y%m%d-%H%M%S"))
        else:
            shutil.rmtree(newrep)
    if not os.path.exists(newrep):
        mkdir_p(newrep)
    if not os.path.exists(os.path.join(dirname, file)):
        cp_p(filename, dirname)

    return os.path.join(dirname, file)

def make_sub_result_rep(image_rep, directory='results'):

    newrep = os.path.join(image_rep, directory)
    if not os.path.exists(newrep):
        mkdir_p(newrep)

    return newrep

def get_im_res(rep, image_name, prefix='sub_', hdr=False):

    image = os.path.join(rep, prefix +  image_name + '.fits')
    if hdr:
        hdu = fits.open(image)[0]
        data, header = hdu.data, hdu.header
        return data, header
    else:
        image = fits.open(image)[0].data
        return image

def get_observer(header):

    if 'TELESCOPE' in header.items():
        observer = header['TELESCOPE']
    else:
        observer = 'GRANDMA'

    return observer
    
def set_results_table(col_names, N_rows):
    
    res_table = Table()
    res_table['image_index'] = np.arange(N_rows)
    for name in col_names:
        res_table[name] = None
    
    return res_table

def get_corner_coords(filename):
    """Get the image coordinates of an image"""

    header = fits.getheader(filename)
    # Get physical coordinates
    Naxis1 = header["NAXIS1"]
    Naxis2 = header["NAXIS2"]

    pix_coords = [[0, 0, Naxis1, Naxis1], [0, Naxis2, Naxis2, 0]]

    # Get physical coordinates
    w = WCS(header)
    ra, dec = w.all_pix2world(pix_coords[0], pix_coords[1], 1)

    return [ra, dec]

def clean_outputs(filenames, outLevel):
    """Delete non required output files"""

    imagelist = np.atleast_1d(filenames)
    for ima in imagelist:
        print("\nCleaning up output files for %s" % ima)
        path = os.path.dirname(ima)
        print(ima)

        rm_p(os.path.join(path, "*.head"))
        if outLevel == 0:
            rm_p('coadd.weight.fits')
            files = glob.glob(path+'/subtraction/*.fits')
            for f in files:
                if '_sub' not in f:
                    rm_p(f)
            for _ in ["*.fits",
                      "*.fit",
                      "*.sh",
                      "subtraction/*mask*",
                      "subtraction/*background",
                      "subtraction/*segmentation"]:
                rm_p(os.path.join(path, _))

        elif outLevel == 1:
            rm_p('coadd.weight.fits')

            for _ in ["subtraction/*mask*",
                      "subtraction/*background",
                      "subtraction/*segmentation"]:
                rm_p(os.path.join(path, _))

        elif outLevel == 2:
            pass
