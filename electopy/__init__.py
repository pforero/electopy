import electopy.loading
import electopy.display
from electopy.electoral_map import electoral_map
from electopy.election import election


def from_mir(year=2016):

    election_dataframe = electopy.loading.load_election(year=year)
    parties, regions, votes, distribution = electopy.loading.clean_mir(election_dataframe)

    electoral_map_object = electoral_map(parties, regions, distribution)

    election_object = election(electoral_map_object, votes)

    return election_object


def from_df(votes, distribution):

    parties, regions, votes, distribution = electopy.loading.clean_df(
        votes, distribution
    )

    electoral_map_object = electoral_map(parties, regions, distribution)

    election_object = election(electoral_map_object, votes)

    return election_object


def compare(election1, election2):

    # Need to check that bot el1 and el2 are type election, and have the same electoral map

    print("Needs to be done")
