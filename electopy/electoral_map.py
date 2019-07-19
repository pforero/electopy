"""Class with the pre-election information of the election.

This class stores the infomation of the election before the results.

"""


class electoral_map:
    """An electoral map before the election takes place.

    The electoral map is all the information known about the election before voting
    takes place. These are: the political parties present in the election, the different
    voting regions, the allocated number of members of parliament every region can
    elect, and the total number of mps in the parliament.

    Parameters
    ----------
    parties: Series
        Political parties in the election.
    regions: Series
        Voting regions in the election.
    distribution: Series
        Allocated distribution of electable mps per voting region.

    Attributes
    ----------
    parties: Series
        Political parties in the election.
    regions: Series
        Voting regions in the election.
    distribution: Series
        Allocated distribution of electable mps per voting region.
    total_mps: int
        Total number of mps in the parliament.


    """

    def __init__(self, parties, regions, distribution):

        if not regions.index.equals(distribution.index):

            raise ValueError("Index of regions do not match the index of distribution")

        self.parties = parties
        self.regions = regions
        self.distribution = distribution

        self.total_mps = _sum_mps(distribution)


def _sum_mps(distribution):
    """Obtain the total number of electable mps in the election.

    Sum all the electable mps for each region to obtain all the mps in play for the
    composition of the parliament.

    Parameters
    ----------
    distribution: Series
        Allocated distribution of electable mps per voting region.

    Returns
    -------
    total: int
        Total number of mps in the parliament.

    """

    total = distribution.sum()

    return total
