# -*- coding: utf-8 -*8-

from setuptools import setup
from setuptools import find_packages


setup(
    name='webshooter-scrapyd-launcher',
    packages=find_packages(),
    package_data={
        'scrapyd_launcher': [],
    },
    version='0.1.0',
    author='Tiago Lira',
    author_email='tiago@intelivix.com',
    entry_points={
        'console_scripts': []
    },
    zip_safe=False,
)
