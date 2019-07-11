from setuptools import setup

requirements = ['pandas', 'numpy', 'geopandas', 'shapely', 'matplotlib']

setup(
    name='electopy',
    version='0.1dev',
    packages=['electopy',],
    license='GNU General Public License v3.0',
    long_description=open('Readme.txt').read(),
    install_requires=requirements,
)
