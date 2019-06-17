import electopy.loading
import electopy.display
from electopy.electoral_map import electoral_map
from electopy.election import election

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import geopandas as gpd

import urllib.request
import zipfile

def from_mir(year=2016):

    df = electopy.loading.load_election(year=year)
    parties, regions, votes, distribution = electopy.loading.clean_mir(df) 

    em = electoral_map(parties,regions,distribution)

    el = election(em,votes)

    return el

def from_df(votes,distribution):

    parties, regions, votes, distribution = electopy.loading.clean_df(votes,distribution) 

    em = electoral_map(parties,regions,distribution)

    el = election(em,votes)

    return el