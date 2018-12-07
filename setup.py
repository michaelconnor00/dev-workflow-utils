# from distutils.core import setup
from setuptools import setup

import cw

setup(
    name='dev-workflow-utils',
    version=cw.VERSION,
    packages=['cw'],
    install_requires=["docopt>=0.6.2"],
    url='',
    license='MIT',
    author='michaelconnor',
    author_email='mike@sparkgeo.com',
    description='SG Tools',
    entry_points={
        'console_scripts': ['cw=cw.cw:main'],
    }
)
