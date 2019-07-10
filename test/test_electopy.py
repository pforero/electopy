import pytest

import electopy
import pandas as pd

# CSV Test

csv_votes=pd.read_csv('past_elections/test_votos.csv',index_col=0,thousands=',')
csv_regions=pd.read_csv('past_elections/test_diputados.csv',squeeze=True,index_col=0)

def test_csv_load():

    el = electopy.from_df(csv_votes,csv_regions)

    assert el.votes.loc[0,0] == 131801

# MIR Test

def test_mir_load():

    el = electopy.from_mir(year=2016)

    assert el.votes.loc[4,0] == 131801

el = electopy.from_mir(year=2016)

def test_mps():

    assert el.mps(4)[0]==3

def test_parlament():

    assert el.parlament().sum() == 350

def test_most_voted():

    assert el.most_voted()[4] == 0

def test_transform():

    el2 = el.transform('PP','PSOE')

    assert el.votes.loc[4,0] != el2.votes.loc[4,0]