import pytest

import electopy
import pandas as pd
import numpy as np

# CSV Test

csv_votes=pd.read_csv('past_elections/test_votos.csv',index_col=0,thousands=',')
csv_regions=pd.read_csv('past_elections/test_diputados.csv',squeeze=True,index_col=0)

def test_csv_load():

    el = electopy.from_df(csv_votes,csv_regions)

    assert el.votes.sum().sum() == 23874674

# MIR Test

def test_mir_load():

    el = electopy.from_mir(year=2016)

    assert el.votes.sum().sum() == 23874674

el = electopy.from_mir(year=2016)

def test_mps():

    assert round(np.linalg.norm(el.mps(4)),2) == 3.74

def test_parlament():

    assert el.parlament().sum() == 350
    assert round(np.linalg.norm(el.parlament()),2) == 171.66

def test_most_voted():

    assert round(np.linalg.norm(el.most_voted()),2) == 10.91

def test_transform():

    el2 = el.transform('PP','PSOE')

    assert all(el2.votes[0] == el.votes[0] + el.votes[1])