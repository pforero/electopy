"""Electopy

This module does simple electoral math for Spain general election results. 
Election results can be obtained directly from Spain's Ministry of Interior or from 
panda's dataframes following a specific format.

"""

import electopy.loading
import electopy.display
from electopy.electoral_map import electoral_map
from electopy.election import election


def from_mir(year=2016):
    """ Create election using the Ministry's of Interior dataset.

    Election results are downloaded directly from the Ministry's of Interior webpage 
    hosting all past election results. The year indicates which election results to 
    download.

    Parameters
    ----------
    year : int
        Year of the election.

    Returns
    -------
    election_object: obj
        An electopy election class.

    Notes
    -----

    The function only accepts years when a general election was held in Spain, since 
    1977.

    """
    election_dataframe = electopy.loading.load_election(year=year)
    parties, regions, votes, distribution = electopy.loading.clean_mir(
        election_dataframe
    )

    electoral_map_object = electoral_map(parties, regions, distribution)

    election_object = election(electoral_map_object, votes)

    return election_object


def from_df(votes, distribution):
    """ Create election using a custom dataframe.

    Election results are downloaded directly from the Ministry's of Interior webpage 
    hosting all past election results. The year indicates which election results to 
    download.

    Parameters
    ----------
    votes : pandas.DataFrame
        DataFrame with the votes for each party (columns) in each voting region (index).
    distribution : pandas.Series
        A priori distribution of allocated members of parliament for each region(index).

    Returns
    -------
    election_object
        An electopy election class.

    """
    parties, regions, votes, distribution = electopy.loading.clean_df(
        votes, distribution
    )

    electoral_map_object = electoral_map(parties, regions, distribution)

    election_object = election(electoral_map_object, votes)

    return election_object


def compare(election1, election2):
    """ None existing function. Needs to be done."""

    # Need to check that bot el1 and el2 are type election, and have the same electoral map

    print("Needs to be done")
