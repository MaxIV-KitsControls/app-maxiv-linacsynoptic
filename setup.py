#!/usr/bin/env python

from setuptools import setup

setup(
    name="taurusgui-linacsynoptic",
    version="1.5.2",
    description="Synoptic for the MAX IV linear accellerator.",
    author="Johan Forsberg",
    author_email="johan.forsberg@maxlab.lu.se",
    license="GPLv3",
    url="http://www.maxlab.lu.se",
    packages=['linacsynoptic'],
    package_data={'linacsynoptic': [
        'resources/index.html',
        'resources/images/*.svg',
        'resources/images/*.png']},
    data_files=[('/usr/share/applications',['maxiv-linac-synoptic.desktop'])],
    install_requires = ['taurus', 'magnetpanel', 'svgsynoptic2'],
    entry_points={
        'console_scripts': [
            'ctlinacsynoptic = linacsynoptic.__main__:main'
        ]
    }
)
