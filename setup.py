#! /usr/bin/env python3
#  coding=utf-8
"""Setup script

run "./setup.py --help-commands" for help.
"""
from datetime import datetime
from os import chdir
from os.path import dirname, abspath, join

from setuptools import setup, find_packages

# Sets Package information
PACKAGE_INFO = dict(
    name='ssl_config',
    description='Mozilla SSL Generator, Python edition',
    long_description_content_type='text/markdown; charset=UTF-8',
    classifiers=[
        # Must be listed on: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: System :: Systems Administration',
        'Topic :: Internet',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ],
    keywords='ssl tls configuration',
    author='J.Goutin',
    url='https://github.com/jgoutin/ssl-config-generator-python',
    project_urls={
        'Documentation': 'https://ssl_config.readthedocs.io',
        'Download': 'https://pypi.org/project/ssl_config',
    },
    license='MPL-2.0',
    python_requires='>=3.5',
    install_requires=[
        'pybars3>0.9.6',
    ],
    setup_requires=['setuptools'],
    tests_require=['pytest', 'requests_html'],
    packages=find_packages(exclude=['docs', 'tests', 'ssl-config-generator']),
    include_package_data=True,
    zip_safe=False,
    command_options={},
    entry_points={'console_scripts': [
        'ssl-config=ssl_config.__main__:_run_command']})

# Gets package __version__ from package
SETUP_DIR = abspath(dirname(__file__))
with open(join(SETUP_DIR, 'ssl_config', '__init__.py')) as source_file:
    for line in source_file:
        if line.rstrip().startswith('__version__'):
            PACKAGE_INFO['version'] = line.split('=', 1)[1].strip(" \"\'\n")
            break

# Gets long description from readme
with open(join(SETUP_DIR, 'README.md')) as source_file:
    PACKAGE_INFO['long_description'] = source_file.read()

# Sphinx configuration
PACKAGE_INFO['command_options']['build_sphinx'] = {
    'project': ('setup.py', PACKAGE_INFO['name'].capitalize()),
    'version': ('setup.py', PACKAGE_INFO['version']),
    'release': ('setup.py', PACKAGE_INFO['version']),
    'copyright': ('setup.py', '2019-%s, %s' % (
        datetime.now().year, PACKAGE_INFO['author']))}

# Runs setup
if __name__ == '__main__':
    chdir(SETUP_DIR)
    setup(**PACKAGE_INFO)
