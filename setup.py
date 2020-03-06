#!/usr/bin/env python
from setuptools import setup

setup(name='epidemic_models',
      description='A simple tool to understand SARS, CoVid etc',
      version='0.1',
      classifiers=['Development Status :: 4 - Beta',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   ],
      long_description=open('README.md').read(),
      url='',
      author_email='lorenzo.busoni@inaf.it',
      author='Lorenzo Busoni',
      license='',
      keywords='SIR',
      packages=['epidemic_models',
                'epidemic_models.utils',
                'epidemic_models.mains'
                ],
      install_requires=["numpy",
                        "openpyxl",
                        ],
      package_data={
          'epidemic_models': ['data/*'],
      },
      include_package_data=True,
      test_suite='test',
      )
