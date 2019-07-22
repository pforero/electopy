"""Pytest for electopy

A series of test using pytest. Tests both, loading by dataframe and from Spain's
Ministry of Interior database.

"""

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
    """Test for election created via dataframe.

    Creates election from dataframe, and then checks the total number of votes.

    """

    el = electopy.from_df(csv_votes, csv_regions)

    vote_sum = el.votes.sum().sum()

    assert vote_sum == 23874674


# MIR Test


def test_mir_load():
    """Test for election created via MIR.

    Creates election from MIR's dataset, and then checks the total number of votes.

    """

    el = electopy.from_mir(year=2016)

    vote_sum = el.votes.sum().sum()

    assert vote_sum == 23874674


el = electopy.from_mir(year=2016)


def test_mps():
    """Test function electopy.mps().

    Checks the number of elected mps for region 4.

    """

    mps_norm = round(np.linalg.norm(el.mps(4)), 2)

    assert mps_norm == 3.74


def test_parliament():
    """Test function electopy.parliament().

    Checks if the total number of elected mps is 350 and the distribution per party
    (does this by using norm).

    """

    total_mps = el.parliament().sum()
    parliament_norm = round(np.linalg.norm(el.parliament()), 2)

    assert total_mps == 350
    assert parliament_norm == 171.66


def test_most_voted():
    """Test function electopy.most_voted().

    Check if the most voted party for all regions.

    """

    most_voted_norm = round(np.linalg.norm(el.most_voted()), 2)

    assert most_voted_norm == 10.91

def test_most_voted_not_nan():
    """Test function electopy.most_voted().

    Check if the name of a party of the most voted is not na.

    """

    party_list = el.most_voted().map(el.parties)

    assert all(~party_list.isna())


def test_transform():
    """Test function electopy.transform().

    Check if the new number of votes for party 0 is the sum of the old votes from
    party 0 and party 1 in the old election. Does this for all regions.

    """

    el2 = el.transform("PP", "PSOE")

    election_votes_diff = el2.votes[0] == el.votes[0] + el.votes[1]

    assert all(election_votes_diff)


def test_spain_map_plot():
    """Test function electopy.spain_map().

    Check if the spain_map plot axis has the correct axis limit dimensions.

    """

    map_plot = el.spain_map(show=False)

    xmin, xmax, ymin, ymax = map_plot.axis()

    assert round(xmin, 2) == -11.94
    assert round(xmax, 2) == 5.11
    assert round(ymin, 2) == 32.08
    assert round(ymax, 2) == 44.35


def test_parliament_composition_plot():
    """Test function electopy.parliament_composition().

    Check if the first wedge from the plot created by parliament_composition has the
    value theta2, corresponding the angle of its representation.

    """

    parliament_plot = el.parliament_composition(show=False)

    assert parliament_plot[0][0].theta2 == 230.9142816066742


# cSpell: ignore votos diputados PSOE MIR's xmin xmax ymin ymax isna
