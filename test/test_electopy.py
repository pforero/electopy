import pytest

import electopy
import pandas as pd
import numpy as np

# CSV Test

csv_votes = pd.read_csv("past_elections/test_votos.csv", index_col=0, thousands=",")
csv_regions = pd.read_csv(
    "past_elections/test_diputados.csv", squeeze=True, index_col=0
)


def test_csv_load():

    el = electopy.from_df(csv_votes, csv_regions)

    vote_sum = el.votes.sum().sum()

    assert vote_sum == 23874674


# MIR Test


def test_mir_load():

    el = electopy.from_mir(year=2016)

    vote_sum = el.votes.sum().sum()

    assert vote_sum == 23874674


el = electopy.from_mir(year=2016)


def test_mps():

    mps_norm = round(np.linalg.norm(el.mps(4)), 2)

    assert mps_norm == 3.74


def test_parlament():

    total_mps = el.parlament().sum()
    parlament_norm = round(np.linalg.norm(el.parlament()), 2)

    assert total_mps == 350
    assert parlament_norm == 171.66


def test_most_voted():

    most_voted_norm = round(np.linalg.norm(el.most_voted()), 2)

    assert most_voted_norm == 10.91


def test_transform():

    el2 = el.transform("PP", "PSOE")

    election_votes_diff = el2.votes[0] == el.votes[0] + el.votes[1]

    assert all(election_votes_diff)


# cSpell: ignore votos diputados PSOE
