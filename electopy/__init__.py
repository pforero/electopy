import electopy.loading
import electopy.electoral_map
import electopy.election

import pandas as pd
import numpy as np

import urllib.request
import zipfile

def from_mir(year=2016):

    df = electopy.loading.load_election(year=year)
    parties, regions, votes, distribution = electopy.loading.clean_df(df) 

    # Seems a bit redundant. Need a nicer way of writting this without repeating itself. The classes should be here?

    em = electopy.electoral_map.electoral_map(parties,regions,distribution)

    el = electopy.election.election(em,votes)

    return el

def compare(el1,el2):

    # Need to check that bot el1 and el2 are type election, and have the same electoral map

    print('Needs to be done')