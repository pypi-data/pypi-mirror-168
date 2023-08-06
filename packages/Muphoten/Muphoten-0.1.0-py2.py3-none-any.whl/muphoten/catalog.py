#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 20:20:44 2020.

@author: duverne
"""

import numpy as np
import numpy.polynomial.polynomial as pl
from astropy.coordinates import SkyCoord
from astropy.stats import sigma_clip
from astropy.table import Table, join, Column
from astropy import units as u
from astroquery.vizier import Vizier
from astroquery.xmatch import XMatch
from muphoten.utils import getpath
from muphoten.photometry import get_source

path_muphoten = getpath()
# from muphoten.utils import CataList
### Starting with some useful functions to manipulate the band and catalog
def u_sdss():
    return ['u', "u'", 'sdss u', 'SDSS u', "sloanu"]

def g_sdss():
    return ['g', "g'", 'sdss g', 'SDSS g', "G'", 'G', "sloang", 'green',
            'sloanG', 'TG', "sG"]

def r_sdss():
    return ['r', "r'", 'sdss r', 'SDSS r', "R'", "sloanr", "sR", "sloanR",
            "SDSSrp+", 'TR', 'SR']

def i_sdss():
    return ['i', "i'", 'sdss i', 'SDSS i', "I'", "sloani","SDSS-i'"]

def z_sdss():
    return ['z', "z'", 'sdss z', 'SDSS z', "Z'", "Z", "sloanz"]

def U_jc():
    return ['U', 'UMag']

def B_jc():
    return ['B', 'BMag']

def V_jc():
    return ['V', 'VMag', '                V']

def R_jc():
    return ['R', 'RMag', 'Rc', '                R', 'Free_R_Free']

def I_jc():
    return ['I', 'IMag', 'Ic']

def c():
    return  ['C', 'c', 'Clear', 'clear', 'cmag',
             'L', 'l', 'Luminance', 'luminance', 'LUM', 'Lum']

def catalog_choice(header):
    """
    Determines the optimal catalog for the calibration.

    Parameters
    ----------
    header : Fits file header.
        Fits file header that have to containn the astrometric informations
        and the band.

    Raises
    ------
    KeyError
        If astrometric keyword or band information
        are not given in the header.
        Either perform astrometric calibation or/and
        use the Muphoten comand line to set the band.

    Returns
    -------
    catalog : str
        catalog index used for the image calibration.

    """

    # Getting astrometric informations.
    if ('CRVAL1' or 'CRVAL2') not in header:
        print
        raise KeyError('No astrometric information found.'
                       'Proceed to astrometric calibration.')
    else:
        ra = header['CRVAL1']
        dec = header['CRVAL2']
    # Getting the band information.
    if 'FILTER' not in header:
        raise KeyError('No filter found in header.')
    else:
        band = header['FILTER']

    # Choosing the catalog.
    rad_deg = 1. * u.arcmin # Check if data are available at the position
    field = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame='icrs')
    z_band = z_sdss()
    u_band = u_sdss()
    B_band = B_jc()
    U_band = U_jc()
    all_u_band = u_sdss() + U_jc()

    if (float(dec) > -30. and band not in all_u_band):
        catalog = 'II/349/ps1' #Use of Pan-STARRS DR 1 as much as possible
        system = 'ps'
        cata_name = 'Pan-STARRS'
    elif Vizier.query_region(field,
                             width=rad_deg,
                             height=rad_deg,
                             catalog="V/147/sdss12")[0]:
        catalog = "V/147/sdss12" # Try SDSS if pan-STARRS is not available
        system = 'sdss'
        cata_name = 'SDSS'

    elif band not in u_band + z_band + U_band + B_band:
        catalog = "I/345/gaia2" # It is impossible to convert GAIA's bands into
                                # SDSS z, or u, nor in U & B jonhson-cousins.
                                # Otherwise, as GAIA is an all sky
        system = 'gaia'         # catalog, it is a good option to calibrate.
        cata_name = 'Gaia'
    elif band : # Else for B, it is possible to use USNO
        catalog = "I/284/out"
        system = 'usno'
        cata_name = 'USNO-B1'
    return catalog, system, cata_name

def CataList():
    cataList = ['Pan-STARRS', 'USNO-B1', 'Gaia', 'SDSS', 'skm']
    return cataList

def getCata(cata_name):
    """
    Return the catalog index used by Vizier and
    the photometric system of the survey.

    Parameters
    ----------
    cata_name : str
        Name of the used catalog.

    Raises
    ------
    KeyError
        If the given catalog name is not in the available one in Muphoten.

    Returns
    -------
    catalog : str
        The catalog index for Vizier request.

    """
    catalist = CataList()
    if cata_name not in catalist:
        raise KeyError('{} not in the avalaible catalogs.'
                       'The available ones are : {}'.format(cata_name,
                                                            catalist))
    else:
        if cata_name == 'Pan-STARRS':
            catalog = 'II/349/ps1'
            system = 'ps'
        elif cata_name == 'USNO-B1':
            catalog = 'I/284/out'
            system = 'usno'
        elif cata_name == 'Gaia':
            catalog = 'I/345/gaia2'
            system = 'gaia'
        elif cata_name == 'skm':
            catalog = 'II/358/smss'
            system = 'skm'
        else:
            catalog = "V/147/sdss12"
            system ='sdss'

    return catalog, system

def get_photmetric_system(band):
    """
    Get the photometric system of the instrument that acquired the image.

    Parameters
    ----------
    band : str
        Name of the filter used top acquire the image.

    Returns
    -------
    system : str
        Name of the sytem in the form use by muphoten.
        jc : Johnson-Cousins (Uc, Bc, vc, Rc, Ic)
        sdss : Sloan Digital Sky Survey
               (u, g, r, i, z - only used for th u band)
        ps : Pan-STARRS (g,r , i, z, y)
        other : Any other filter, most probably unfiltered (ie : clear) or
                Luminance, very close to clear image, with cuts in soft UV
                and NIR
    """
    if band in ['UMag', 'BMag', 'VMag', 'RMag','IMag']:
        system = ['jc']
    elif band in ['umag']:
        system = ['sdss', 'skm']
    elif band in ['gmag', 'rmag', 'imag', 'zmag']:
        system = ['ps', 'sdss', 'skm']
    else:
        system = ['other']

    return system

def get_filter(header, band=None):
    """
    Find the filter used to take an image or turn a given given band into \
    a form that can be used for the calibration.

    Parameters
    ----------
    header : header object
        Header of an image.
    band : str, optional
        if the filter is not in the header it can be given here.
        The default is None.

    Raises
    ------
    ValueError
        No filter found is the header or in given.

    Returns
    -------
    band : string
        band in a form that can be used for the calibration.

    """
    if band is not None:
        band = band
    else:
        try:
            band = header['FILTER']
        except Exception:
            raise ValueError('No filter found nor given')

    u_band = u_sdss()
    g_band = g_sdss() #Different names that can be
    r_band = r_sdss() #found in header
    i_band = i_sdss()
    z_band = z_sdss()
    V_band = V_jc() #Different names that can be
    R_band = R_jc() #found in header
    I_band = I_jc()
    B_band = B_jc()
    U_band = U_jc()
    clear = c()
    if band in u_band:
        band = 'umag'
    if band in g_band:
        band = 'gmag'
    if band in r_band:
        band = 'rmag'
    if band in i_band:
        band = 'imag'
    if band in z_band:
        band = 'zmag'
    if band in U_band:
        band = 'UMag'
    if band in B_band:
        band = 'BMag'
    if band in V_band:
        band = 'VMag'
    if band in R_band:
        band = 'RMag'
    if band in I_band:
        band = 'IMag'
    if band in clear:
        band = 'cmag'

    return band

### Catalog requests & manipulations of the results ###
def source_coordinates(source_table):
    """
    Give the coordinates of the detected sources in the convenient form for \
    XMatch method.

    Parameters
    ----------
    source_table : astropy.table
        Table containing the informations about detected sources.
        It must contain a sky localisation Column.

    Returns
    -------
    coord_sources : astropy.table
        Table with three columns RA and DEC in degrees and an index.

    """
    coord_sources = Table([source_table['sky_centroid'].ra.deg,
                          source_table['sky_centroid'].dec.deg],
                          names=('_RAJ2000', '_DEJ2000'))
    coord_sources['idx'] = np.arange(len(coord_sources))

    return coord_sources

def xmatch(coordinates, catalog, radius, col_name=['_RAJ2000', '_DEJ2000'] ):
    """
    Perform cross-match with a catalog using the CDS XMatch.

    Parameters
    ----------
    coordinates : astropy.table
        RA, DEC of all detected sources.
    catalog : str
        Vizier identifier of the catalog.
    radius : Float
        radius in arcsecond of the area where to perform the request.

    Returns
    -------
    matched_stars : astropy.table
        The objects in the catalog that matched with the coordinates.

    Notes
    -----
    Vizier catalog identifiers:
    Gaia DR2: I/345/gaia2
    SDSS DR12: V/147/sdss12
    2MASS: II/246/out
    USNO B1: I/284/out
    USNO A2: I/252/out
    GLADE 2: VII/281/glade2
    Panstarrs DR1: II/349/ps1
    Skymaper DR1 : II/358/smss
    """
    matched_stars = XMatch.query(coordinates,
                                 cat2='vizier:%s' % catalog,
                                 max_distance=radius * u.arcsec,
                                 colRA1=col_name[0],
                                 colDec1=col_name[1])

    return matched_stars

def joining(source, matched_star):
    """
    Join a catalog of sources detected in a image and a catalog of objects \
    detected in a reference survey.

    Parameters
    ----------
    source : astropy.table
        Table with the sources detected in an image.
    matched_star : astropy.table
        Table with the objects detected in the survey.

    Returns
    -------
    source : astropy.table
        Join table of the two argument tables.

    """
    flag = np.zeros(len(matched_star))
    matched_star['id'] = np.arange(len(matched_star))
    referenced_star_idx = np.unique(matched_star['idx'])
    closest_id = []
    for idx in referenced_star_idx:
        mask = matched_star['idx'] == idx
        closest_id.append(matched_star[mask]['id'][0])
    # Keep only the closest object in matched_star to a source in the image
    flag[closest_id] = 1
    ref_sources = matched_star[flag == 1]
    source = join(source, ref_sources, keys='idx')

    return source

def cleaning_PS(source):
    """
    Remove the object with bad photometry in a Pan-STARRS table.

    Parameters
    ----------
    source : astropy.table
        Table with the information of PAN-STARRS.

    Returns
    -------
    source : astropy.table
        Table without objects flagged with a poor photometry.

    """
    # Quality for PAN STARRS
    flag = Column(name='Flag Binary',
                  data=np.ones_like(source['Qual'],
                  dtype='a8'))
    source.add_column(flag)
    mask = np.ones_like(source['Qual'], dtype = bool)
    for i, flag in enumerate(source['Qual']):
        bin_flag = bin(source['Qual'][i])[2:].zfill(8)
        source['Flag Binary'][i] = bin_flag
        if bin_flag[-1] == '1' or bin_flag[-3] == '0' or bin_flag[-5] == '0' \
        or bin_flag[-7] == '1' or bin_flag[0] == '1':
        #removing extended objects with first condition
        #removing bad measurement with the second
        #removing objects with bad quality stack
        #removing suspect objects in the stack
        #removing poor quality stack objects
            mask[i] = False
    source = source[mask]

    return source

def cleaning_gaia(source):
    """
    Remove the bad quality photomety objects in the Gaia table returned by
    the crossmatch with the catalog.
    Are considered bad quality objects:
        - duplicated source
    See here for details about the column names :
        https://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=I/345

    Parameters
    ----------
    source : astropy table
        Table return after a crossmatch with Gaia via the vizier portal.

    Returns
    -------
    source : astropy table
        Input table without the rejected objects.

    """
    source = source[source['duplicated_source']==0]

    return source

def cleaning_sdss(source):
    """
    Remove the bad quality photomety objects in the SDSS table returned by
    the crossmatch with the catalog.
    Are considered bad quality objects:
        - q_mode : indicate the quualitu of the photometry.
                   We keep only the objects with value "+"(good photoometry).
        - Q : Quality of teh observation.
              We keep only objects with value 3 (good observations).
        - class : nature of the object star or galaxy.
                  We keep only objects with value 6 (stars).
        - flag to remove (Hexadecimal values):
            - saturated objects
            - objets on the edge
            - blended objects
            - moving objects

    See here for details about the column names :
        https://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=V/147

    Parameters
    ----------
    source : astropy table
        Table return after a crossmatch with SDSS DR 12 via the vizier portal.

    Returns
    -------
    source : astropy table
        Input table without the rejected objects.

    """
    cleaning_mask = (source['Q']==3)
    #cleaning_mask &= (source['q_mode']=='+')
    cleaning_mask &= (source['class']==6)
    # pkl = open(path_muphoten +'/sdss_flags_list.pkl', "rb")
    # hexa_flag = pickle.load(pkl) # list with all the flags for the DR12
    hexa_flag = [#(4, 'EDGE'),
                 #(8, 'BLENDED'),
                 (262144, 'SATURATED'),
                 (2147483648, 'MOVED')] # flags to remove
    source['hexa_flags'] = [int('0x' + str(i),16) for i in source['flags']]
    source['to_flags'] = 0
    for i, _ in enumerate(source['hexa_flags']):
        for fid, _ in hexa_flag:
            if i&fid>0:
                source['to_flags'][i]=1
                print(i)
                print(_)
                print(fid)
    cleaning_mask &= (source['to_flags']==0)
    source = source[cleaning_mask]

    return source

def cleaning_usno(source):
    """
    Remove the bad quality photomety objects in the USNO-B1 table returned by
    the crossmatch with the catalog.
    Are considered bad quality objects:
        - Object on a diffraction spike

    See here for details about the column names :
        https://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=I/284

    Parameters
    ----------
    source : astropy table
        Table return after a crossmatch with USNO-B1 via the vizier portal.

    Returns
    -------
    source : astropy table
        Input table without the rejected objects.

    """
    source['to_flag'] = [1 if 's' in i else 0 for i in source['Flags']]

    return source

def cleaning_crossmatch(cata, phot_table):
    """
    Remove the bad quality objects in the crossmatched table according
    to the chosen catalog.

    Parameters
    ----------
    cata : str
        Vizier index of the catalog used fo rthe calibration.
    phot_table : astropy table
        Table to clean.

    Returns
    -------
    phot_table : astropy table
        Cleaned table.

    """
    if cata=='II/349/ps1':
        phot_table = cleaning_PS(phot_table)
    if cata=='V/147/sdss12':
        phot_table = cleaning_sdss(phot_table)
    if cata=='I/345/gaia2':
        phot_table = cleaning_gaia(phot_table)
    if cata=='I/284/out':
        phot_table = cleaning_usno(phot_table)

    return phot_table

### Catalog requests & manipulations of the results ###
### Functions to compute different photometric transformation laws  ###
def poly(x, coefficients):
    """
    Compute a polynome, useful for transformation laws.

    Parameters
    ----------
    x : list or array like quantity
        Variable or the polynome.
    coefficients : list or array like quantity
        Coefficient of the polynome.

    Returns
    -------
    polys : list or array like quantity
        Result of the polynome computation.

    """
    polys = 0
    for i, coef in enumerate(coefficients):
        polys += coef * x**i

    return polys

def from_gaia2Johnson(band, Gaia_Table):
    """
    Give the transformation laws to go from gaia photometric system \
    to Johnson-Cousins photometric system\
    Transformation given by https://gea.esac.esa.int/archive/documentation/ \
    GDR2/Data_processing/chap_cu5pho/sec_cu5pho_calibr/ \
    ssec_cu5pho_PhotTransf.html \
    Table 5.8 \
    WARNING : GAIA's Magnitudes are in Vega.

    Parameters
    ----------
    band: band used to get the image
    Gaia_Table: astropy.table with information from Gaia for
    the sources in the image

    Returns
    -------
    Results : QTable with informations from Gaia and the computation
             for the band of the image
    """
    V_band = V_jc() #Differen15.690t names that can be
    R_band = R_jc() #found in header
    I_band = I_jc()
    B_band = B_jc()

    if band in V_band:
        mask = (-0.5 < Gaia_Table['bp_rp'])
        Result = Gaia_Table[mask]
        mask = (Result['bp_rp'] < 2.75)
        Result = Result[mask] #Validity of the transformation law
        coefficients = [-0.01760, -0.006860, -0.1732]
        Result["VMag"] = Result["phot_g_mean_mag"] - poly(Result['bp_rp'],
                                                            coefficients)
        Result["error"] = 0.045858

    if band in R_band:
        mask = (-0.5 < Gaia_Table['bp_rp'])
        Result = Gaia_Table[mask]
        mask = (Result['bp_rp'] < 2.75)
        Result = Result[mask] #Validity of the transformation law
        coefficients = [-0.003226, 0.3833, -0.1345]
        Result["RMag"] = Result["phot_g_mean_mag"] - poly(Result['bp_rp'],
                                                            coefficients)
        Result["error"] = 0.04840

    if band in I_band:
        mask = (-0.5 < Gaia_Table['bp_rp'])
        Result = Gaia_Table[mask]
        mask = (Result['bp_rp'] < 2.75)
        Result = Result[mask] #Validity of the transformation law
        coefficients = [0.02085, 0.7419, -0.09631]
        Result["IMag"] = Result["phot_g_mean_mag"] - poly(Result['bp_rp'],
                                                            coefficients)
        ########Revoir cette derniere transformation, pt etre mal implementee
        Result["error"] = 0.04956

    if band in B_band:
        raise ValueError('No transformation law for Gaia->B_Jonhson')

    return Result

def from_gaia2SDSS(band, Gaia_Table):
    """
    Give the transformation laws to go from gaia photometric system
    to SDSS photometric system
    Transformation given by https://gea.esac.esa.int/archive/documentation/
    GDR2/Data_processing/chap_cu5pho/sec_cu5pho_calibr/
    ssec_cu5pho_PhotTransf.html
    Table 5.7
    WARNING : GAIA's Magnitudes are in the Vega system

    parameters: band: band used to get the image
                Gaia_Table: astropy.table with information from Gaia for
                the sources in the image.

    returns: astropy.table with informations from Gaia and the computation
             for the band of the image
    """
    u_band = u_sdss()
    g_band = g_sdss() #Different names that can be
    r_band = r_sdss() #found in header
    i_band = i_sdss()
    z_band = z_sdss()

    if band in r_band:
        mask = (Gaia_Table['bp_rp'] > 0.2)
        Result = Gaia_Table[mask]
        mask = (Result['bp_rp'] < 2.7)
        Result = Result[mask] #Validity of the transformation law
        coefficients = [-0.12879, 0.24662, -0.027464, -0.049465]
        Result["rmag"] = Result["phot_g_mean_mag"] - poly(Result['bp_rp'],
                                                          coefficients)
        Result["error"] = 0.066739

    if band in i_band:
        mask = (Gaia_Table['bp_rp'] > 0.0)
        Result = Gaia_Table[mask]
        mask = (Result['bp_rp'] < 4.5)
        Result = Result[mask] #Validity of the transformation law
        coefficients = [-0.29676, 0.64728, -0.10141, 0.]
        Result["imag"] = Result["phot_g_mean_mag"] - poly(Result['bp_rp'],
                                                            coefficients)
        Result["error"] = 0.098957

    if band in g_band:
        mask = (-0.5 < Gaia_Table['bp_rp'])
        Result = Gaia_Table[mask]
        mask = (Result['bp_rp'] < 2.0)
        Result = Result[mask] #Validity of the transformation law
        coefficients = [0.13518, -0.46245, -0.25171, 0.021349]
        Result["gmag"] = Result["phot_g_mean_mag"] - poly(Result['bp_rp'],
                                                            coefficients)
        Result["error"] = 0.16497

    if band in z_band:
        raise ValueError('No transformation law for Gaia->z_sdss')

    if band in u_band:
        raise ValueError('No transformation law for Gaia->u_sdss')

    return Result

def from_PS2clear(band, PS_Table):

    c_band = c()
    if band in c_band:
        PS_Table['flux_r'] = 3631 * 10**(-0.4 * PS_Table["rmag"])
        PS_Table['flux_g'] = 3631 * 10**(-0.4 * PS_Table["gmag"])
        PS_Table['cmag'] = -2.5 * np.log10((PS_Table['flux_r'] +
                                            PS_Table['flux_g']) / 3631)
        PS_Table['error'] = np.sqrt((PS_Table['flux_r'] / (PS_Table['flux_g'] + 
                                     PS_Table['flux_r']))**2 * PS_Table["e_rmag"]**2 + 
                                    (PS_Table['flux_g'] / (PS_Table['flux_g'] + 
                                     PS_Table['flux_r']))**2 * PS_Table["e_gmag"]**2)

    return PS_Table

def from_skm2clear(band, skm_Table):

    c_band = c()
    if band in c_band:
        skm_Table['flux_r'] = 3631 * 10**(-0.4 * skm_Table["rPSF"])
        skm_Table['flux_g'] = 3631 * 10**(-0.4 * skm_Table["gPSF"])
        skm_Table['cmag'] = -2.5 * np.log10((skm_Table['flux_r'] +
                                             skm_Table['flux_g']) / 3631)
        skm_Table['error'] = np.sqrt((skm_Table['flux_r'] / (skm_Table['flux_g'] + 
                                     skm_Table['flux_r']))**2 * skm_Table["e_rPSF"]**2 + 
                                    (skm_Table['flux_g'] / (skm_Table['flux_g'] + 
                                     skm_Table['flux_r']))**2 * skm_Table["e_gPSF"]**2)

    return skm_Table

def from_PS2Johnson(band, PS_Table):

    V_band = V_jc() #Different names that can be
    R_band = R_jc() #found in header
    I_band = I_jc()
    B_band = B_jc()

    if band in R_band:
        coefficients = [-0.163, -0.086, -0.061]
        PS_Table['g-r'] = PS_Table['gmag'] - PS_Table['rmag']
        PS_Table["RMag"] = PS_Table["rmag"] + poly(PS_Table['g-r'],
                                                   coefficients)
        PS_Table["error"] = 0.041

    if band in V_band:
        coefficients = [-0.020, -0.498, -0.008]
        PS_Table['g-r'] = PS_Table['gmag'] - PS_Table['rmag']
        PS_Table["VMag"] = PS_Table["gmag"] + poly(PS_Table['g-r'],
                                                   coefficients)
        PS_Table["error"] = 0.032

    if band in B_band:
        coefficients = [0.199, 0.540, 0.016]
        PS_Table['g-r'] = PS_Table['gmag'] - PS_Table['rmag']
        PS_Table["BMag"] = PS_Table["gmag"] + poly(PS_Table['g-r'],
                                                   coefficients)
        PS_Table["error"] = np.sqrt((PS_Table['e_gmag']**2 *\
                                    (1 + coefficients[-2] +
                                     2*coefficients[-1]*PS_Table['g-r'])**2) +
                                    (PS_Table['e_rmag']**2 *\
                                    (2*coefficients[-1]*PS_Table['g-r'] +
                                     coefficients[-2])**2))
        # PS_Table["error_transfo"] = np.sqrt((PS_Table['e_gmag']**2 +
                                              # PS_Table['e_rmag']**2)) *
                                              # (2*coefficients[-1]*
                                              # PS_Table['g-r'] +
                                              # coefficients[-2])
    if band in I_band:
        coefficients = [-0.387, -0.123, -0.03]
        PS_Table['g-r'] = PS_Table['gmag'] - PS_Table['rmag']
        PS_Table["IMag"] = PS_Table["imag"] + poly(PS_Table['g-r'],
                                                   coefficients)
        PS_Table["error"] = 0.054

    return PS_Table

def from_usno2Johnson(band, USNO_Table):
    """
    Give the transformation laws to go from USNO photometric system
    to Johnson photometric system
    Transformation given by http://www.mpe.mpg.de/~jcg/GROND/calibration.html

    parameters: band: band used to get the image
                USNO_Table: astropy.table with information from USNO for
                the sources in the image.

    returns: astropy.table with informations from USNO and the computation
             for the band of the image.
    """
    V_band = V_jc() #Different names that can be
    R_band = R_jc() #found in header
    I_band = I_jc()
    B_band = B_jc()

    if band in V_band:
        USNO_Table['VMag'] = (0.444 * USNO_Table['B1mag'] +
                              0.556 * USNO_Table['R1mag'])
        USNO_Table["error_from_transformation"] = 0.5
    if band in B_band:
        USNO_Table['BMag'] = USNO_Table['B1mag']
        USNO_Table["error"] = 0.5
    if band in R_band:
        USNO_Table['RMag'] = USNO_Table['R1mag']
        USNO_Table["error"] = 0.5
    if band in I_band:
        USNO_Table['IMag'] = USNO_Table['Imag']
        USNO_Table["error"] = 0.5
#        raise ValueError('No transformation law known for USNO->I_Johnson')

    return USNO_Table

def from_SDSS2Johnson(band, SDSS_Table):
    """
    Give the transformation laws to go from SDSS photometric system
    to Johnson photometric system
    Transformation given by http://www.sdss3.org/dr8/algorithms/
    sdssUBVRITransform.php

    parameters: band: band used to get the image
                SDSS_Table: astropy.table with information from SDSS for
                the sources in the image

    returns: astropy.table with informations from SDSS and the computation
             for the band of the image
    """
    V_band = V_jc() #Different names that can be
    R_band = R_jc() #found in header
    I_band = I_jc()
    B_band = B_jc()
    U_band = U_jc()

    if band in V_band:
        coefficients = [- 0.016, -0.573]
        SDSS_Table['g-r'] = SDSS_Table['gmag'] - SDSS_Table['rmag']
        SDSS_Table["VMag"] = SDSS_Table["gmag"] + poly(SDSS_Table['g-r'],
                                                            coefficients)
        SDSS_Table["error"] = np.sqrt((0.002 * SDSS_Table['g-r'])**2 +
                                              0.573**2 * SDSS_Table['e_rmag']**2
                                              + 0.427**2 * SDSS_Table['e_gmag']**2
                                              + 0.002**2)

    if band in R_band:
        coefficients = [0.152, -0.257]
        SDSS_Table['r-i'] = SDSS_Table['rmag'] - SDSS_Table['imag']
        SDSS_Table["RMag"] = SDSS_Table["rmag"] + poly(SDSS_Table['r-i'],
                                                            coefficients)
        SDSS_Table["error"] = np.sqrt(0.743**2 *SDSS_Table['e_rmag']**2+
                                              0.257**2 *SDSS_Table['e_imag']**2+
                                              0.002**2 +
                                              SDSS_Table['r-i']**2 * 0.004**2)


    if band in I_band:
        coefficients = [-0.394, -0.409]
        SDSS_Table['i-z'] = SDSS_Table['imag'] - SDSS_Table['zmag']
        SDSS_Table["IMag"] = SDSS_Table["imag"] + poly(SDSS_Table['i-z'],
                                                            coefficients)
        SDSS_Table["error"] = np.sqrt(0.591**2 *SDSS_Table['e_imag']**2+
                                              0.409**2 *SDSS_Table['e_zmag']**2+
                                              0.002**2 +
                                              SDSS_Table['i-z']**2 * 0.006**2)

    if band in B_band:
        coefficients = [0.219, 0.312]
        SDSS_Table['g-r'] = SDSS_Table['gmag'] - SDSS_Table['rmag']
        SDSS_Table["BMag"] = SDSS_Table["gmag"] + poly(SDSS_Table['g-r'],
                                                            coefficients)
        SDSS_Table["error"] = np.sqrt(1.312**2 * SDSS_Table['e_gmag']**2 +
                                              0.312**2 * SDSS_Table['e_rmag']**2 +
                                              0.002**2 +
                                              SDSS_Table['g-r']**2 * 0.003**2)
    if band in U_band:
        raise ValueError('No transformation law for SDSS -> U')

    return SDSS_Table

def change_photometric_system(image_phot_syst, cata_phot_syst,
                              band, phot_table):

    if cata_phot_syst == 'ps':
        if 'jc' in image_phot_syst:
            print('Changing from Pan-STARRS photometric \n'
                  'system to Johnson-Cousins')
            phot_table = from_PS2Johnson(band, phot_table)
        if 'other' in image_phot_syst:
            print('Changing from Pan-STARRS photometric \n'
                  'system to Unfiltered')
            phot_table = from_PS2clear(band, phot_table)
    if cata_phot_syst == 'sdss':
        if 'jc' in image_phot_syst:
            print('Changing from SDSS photometric\
                  system to Johnson-Cousins')
            phot_table = from_SDSS2Johnson(band, phot_table)
        if 'other' in image_phot_syst:
            print('Changing from SDSS photometric \n'
                  'system to Unfiltered')
            phot_table = from_PS2clear(band, phot_table)
    if cata_phot_syst == 'gaia':
        if 'jc' in image_phot_syst:
            print()
            phot_table = from_gaia2Johnson(band, phot_table)
        if ('sdss' or 'ps') in image_phot_syst:
            print('Changing from Gaia photometric \n'
                  'system to SDSS/Pan-STARRS')
            phot_table = from_gaia2SDSS(band, phot_table)
        if 'other' in image_phot_syst:
            raise ValueError('No transformation law for Gaia -> Unfiltered')
    if cata_phot_syst == 'usno':
        if 'jc' in image_phot_syst:
            print('from usno to jc')
            print('Changing from USNO-B1 photometric \n'
                  'system to Johnson-Cousins')
            phot_table = from_usno2Johnson(band, phot_table)

        else:
            raise ValueError('No transformation law\
                             for USNO-B1 -> {}'.format(image_phot_syst[0]))
    if cata_phot_syst == 'skm':
        phot_table = from_skm2clear(band, phot_table)

        return phot_table

def calibration(source, catalog, cata_phot_syst, stars, wcs_data,
                n_sigma=2.0, header=None, cut_mag=21., band=None):

    if band is None:
        band = get_filter(header)
    image_phot_syst = get_photmetric_system(band)
    coord_sources = source_coordinates(source)
    crossmatch = xmatch(coord_sources, catalog, 5.0)
    source = joining(source, crossmatch)

    star = get_source(source, stars, wcs_data)
    source = cleaning_crossmatch(catalog, source)
    if cata_phot_syst not in image_phot_syst:
        change_photometric_system(image_phot_syst,
                                  cata_phot_syst,
                                  band, source)
    else:
        source['error'] = source['e_'+ band]
        star['error'] = star['e_'+ band]
    if cut_mag!=0:
        mask_magnitude = (source[band] < cut_mag)
        source = source[mask_magnitude]
    source.sort('Magnitude')
    source['Delta_Mag'] = source[band] - source['Magnitude']
    clip = sigma_clip(source['Delta_Mag'], sigma=n_sigma, masked=True)
    clip_mask = np.invert(clip.recordmask)
    source = source[clip_mask]

    coefs, V = np.ma.polyfit(source['Magnitude'], source[band],
                             1, cov=True)
    source['Calibrated_Mag'] = pl.polyval(source['Magnitude'],
                                          np.flip(coefs))
    da_2, db_2 = V[0,0], V[1,1]
    if band not in star.columns:
        if cata_phot_syst not in image_phot_syst:
            change_photometric_system(image_phot_syst,
                                      cata_phot_syst,
                                      band, star)
    star['Calibrated_Mag'] = pl.polyval(star['Magnitude'],
                                          np.flip(coefs))
    return source, coefs, da_2, db_2, star

def from_Vega2AB(band, mag_table):
    """
    Give the transformation laws to go from Vega system to AB system
    Transformation given by http://www.astronomy.ohio-state.edu/
    ~martini/usefuldata.html
    Based on Blanton et al. (2007)

    parameters: band: band used to get the image.
                mag_Table: astropy.table with magnitued in Vega system.

    returns: astropy.table with informations from PS and the computation
             for the band of the image.
    """
    V_band = V_jc() #Different names that can be
    R_band = R_jc() #found in header
    I_band = I_jc()
    B_band = B_jc()
    g_band = g_sdss() #Different names that can be
    r_band = r_sdss() #found in header
    i_band = i_sdss()
    z_band = z_sdss()

    #Conversion for Johnson-Cousins photometric System
    if band in V_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] + 0.02
    if band in B_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] - 0.09
    if band in R_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] + 0.21
    if band in I_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] + 0.45

    #Conversion for sdss/Pan-STARRS photometric System
    if band in g_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] - 0.08
    if band in r_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] + 0.16
    if band in i_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] + 0.37
    if band in z_band:
        mag_table['magnitude_AB'] = mag_table['magnitude'] + 0.54

    return mag_table
