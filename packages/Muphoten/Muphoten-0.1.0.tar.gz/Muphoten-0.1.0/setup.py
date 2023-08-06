#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import glob

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['astropy>=4.3.1',
                'astroquery>=0.4.4.dev7007',
                'Bottleneck>=1.3.2',
                'hjson>=3.0.2',
                'matplotlib>=3.4.3',
                'numpy>=1.21.2',
                'photutils==1.2.0',
                'regions>=0.5',
                'xmltodict>=0.12.0',
                'scikit-image>=0.18.3',
                'scipy>=1.7.1',
                'shapely']

setup_requirements = [ ]

test_requirements = [ ]

data_files = [("ps1_survey", ["muphoten/ps1_survey/ps1grid.fits"]),
              ("config", glob.glob("muphoten/config/*/*"))]

setup(
    author="Pierre-Alexandre Duverne, David Corre",
    author_email='duverne@protonmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A photometry tool for transient astromy"
                "design for network of telescopes.",
    entry_points={'console_scripts': ['mu_bkg_subtraction=muphoten.cli.background_subtraction:main',
                                      'mu_mag_lim=muphoten.cli.mag_lim:main',
                                      'mu_photometry=muphoten.cli.photometry:main',
                                      'mu_psf=muphoten.cli.psf:main',
                                      'mu_sanitise=muphoten.cli.sanitise:main',
                                      'mu_subtraction=muphoten.cli.subtraction:main']},
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['photometry', 'transient', 'astronomy'],
    name='Muphoten',
    packages=find_packages(include=['muphoten', 'muphoten.*']),
    data_files=data_files,
    setup_requires=setup_requirements,
    # test_suite='tests',
    # tests_require=test_requirements,
    url='https://gitlab.in2p3.fr/icare/MUPHOTEN',
    version='0.1.0',
    zip_safe=False)
