# -*- coding: utf-8 -*-

# HACK for `nose.collector` to work on python 2.7.3 and earlier
import multiprocessing
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'boto3',
    'configparser >= 5.3',
    'gatilegrid == 0.2.0',
    'pyproj >= 3.3',
]


setup(name=u'tool_aws',
      version=u'0.2.6',
      description=u'AWS scripts for geoadmin',
      author=u'Andrea Borghi, Loic Gasser',
      author_email=u'andrea.borghi@swisstopo.ch, loicgasser4@gmail.com',
      license=u'BSD-2',
      url=u'https://github.com/geoadmin/tool-aws.git',
      packages=find_packages(exclude=['tests']),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Scientific/Engineering :: GIS',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=install_requires,
      python_requires='>=3.6, <4',
      entry_points={
          'console_scripts': [
              's3rm=tool_aws.s3.rm:main',
          ]
      },
      )
