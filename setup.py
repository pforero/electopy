from setuptools import setup

requirements = ['pandas', 'numpy', 'geopandas', 'shapely', 'matplotlib']

setup(
    name='electopy',
    version='0.1dev',
    packages=['electopy',],
    description='A simple tool in Python used to look and analyse General Election Results in Spain',
    license='GNU General Public License v3.0',
    url='https://github.com/pforero/electopy',
    long_description=open('Readme.txt').read(),
    install_requires=requirements,
)
