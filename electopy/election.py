"""Class with the information of a general election

Elections are the main class in electopy. They contain all the attributes of the 
election (voting regions, political parties and votes per region per party). They also
contain the methods for election analysis.

"""

import electopy
import electopy.display
import electopy.electoral_map

import pandas as pd
import numpy as np

from matplotlib.colors import ListedColormap


class election:
    """A Spanish general election.

    The election is the main class object of electopy. It represents a general election
    in Spain and contains the methods to analyze the election results.

    Parameters
    ----------
    electoral_map: obj
        Electoral map of the election before voting.
    votes: DataFrame
        Votes per region per party in the election result.

    Attributes
    ----------
    electoral_map: obj
        Electoral map of the election before voting.
    votes: DataFrame
        Votes per region per party in the election result.
    parties: Series
        Political parties in the election.
    regions: Series
        Voting regions in the election.
    distribution: Series
        Allocated distribution of electable mps per voting region.


    """

    def __init__(self, electoral_map, votes):

        if not isinstance(electoral_map, electopy.electoral_map):

            raise ValueError(
                "Not an Electoral Map: electoral_map is not of class electoral_map"
            )

        if not votes.columns.equals(electoral_map.parties.index):

            raise ValueError(
                "votes columns do not match the parties of the electoral map"
            )

        if not votes.index.equals(electoral_map.regions.index):

            raise ValueError(
                "votes index does not match the regions of the electoral map"
            )

        self.electoral_map = electoral_map
        self.votes = votes

        self.parties = electoral_map.parties
        self.regions = electoral_map.regions
        self.distribution = electoral_map.distribution

    def mps(self, region):
        """Get the members of parties elected for each party in a region.

        The mps per party are calculated using the D'Hondt method 
        (https://en.wikipedia.org/wiki/D%27Hondt_method).

        Parameters
        ----------
        region: int
            Region for which the distribution of mps per party is calculated.

        Returns
        -------
        mps_allocated: Series
            Elected mps for each political party in the region.

        """

        # This should allow you to chose for which parties and which regions you get the result

        fraction_per_mp = np.array(
            [1 / i for i in range(1, self.distribution[region] + 1)]
        )

        df = (
            self.votes.loc[region]
            .apply(lambda votes_per_party: votes_per_party * fraction_per_mp)
            .apply(pd.Series)
            .unstack()
            .sort_values(ascending=False)[: self.distribution[region]]
        )

        mps_allocated = df.index.get_level_values(1).value_counts()

        # It should return ALL parties mps chosen, not just with those with a value > 0

        return mps_allocated

    def parlament(self):
        """Parlament composition from the election.

        Calculates the total mps for each political party in the parliament. Does this 
        by calculating the mps for each voting region and adding them by party.

        Returns
        -------
        total_mps
            Total number of elected mps for each political party.

        """

        mps_per_region = self.votes.apply(
            lambda votes_per_region: self.mps(votes_per_region.name), axis=1
        ).replace(np.nan, 0)

        total_mps = mps_per_region.sum().astype(int)

        return total_mps

    def most_voted(self):
        """The party with more votes for each region.

        Returns which political party obtains the most votes in each voting region.

        Returns
        -------
        most_voted: Series
            Party with the most votes in each region.

        """

        most_voted = self.votes.apply(_most_voted_party, axis=1)

        return most_voted

    def spain_map(self, canary_x=7, canary_y=5, text=""):
        """Display a map of Spain with the most voted party in each region.

        Creates and displays a map of Spain representing the most voted party in each
        voting region.

        Parameters
        ----------
        canary_x: float
            X-coordinate move of the Canary Islands from original position
        canary_y: float
            Y-coordinate move of the Canary Islands from original position
        text: str
            Additional text to add to the plot title

        """

        spain_geo_dataframe = electopy.display.get_spain_map(x=canary_x, y=canary_y)

        spain_geo_dataframe = electopy.display.proper_names(spain_geo_dataframe)

        most_voted_party_per_region = pd.DataFrame(
            data=self.most_voted().map(self.parties).values,
            index=self.most_voted().index.map(self.regions),
        )

        geo_and_most_voted = spain_geo_dataframe.join(most_voted_party_per_region)

        colormap = ListedColormap(
            electopy.display.create_colors(
                self.most_voted().map(self.parties).sort_values().unique()
            )
        )

        electopy.display.create_map_plot(geo_and_most_voted, colormap, text)

    def parlament_composition(self, text=""):
        """Display composition of the parlmanet by elected mps for each political party.

        Creates and displays a pie chart with the representation of the number of
        elected mps in the parlament for each political party.

        Parameters
        ----------
        text: str
            Additional text to add to the plot title
        
        """

        sorted_parlament = self.parlament().sort_values(ascending=False)

        labels = electopy.display.create_parlament_labels(
            sorted_parlament.rename(self.parties)
        )

        colors = electopy.display.create_colors(
            sorted_parlament.rename(self.parties).index
        )

        electopy.display.create_parlament_plot(sorted_parlament, colors, labels, text)

    def transform(self, party_benefiting, party_losing, weight=1.0):
        """Create a new election by changing the results of the election.

        Creates a new election object which shares the same electoral map as the
        election, but changes the result with a shift of votes from the losing party to
        the benefiting party.

        Parameters
        ----------
        party_benefiting: str
            Name of the political party which gets a positive influx of votes.
        party_losing: str
            Name of the political party which gets a negative influx of votes.
        weight: float
            Share of votes from the losing party which goes to the benefiting party.

        Returns
        -------
        election: obj
            An electopy election class.

        """

        # Needs to find a new way to do (and store parameters) transformations

        party_benefiting_code = self.parties[self.parties == party_benefiting].index[0]
        party_losing_code = self.parties[self.parties == party_losing].index[0]

        new_votes = _new_result(
            self.votes.copy(), party_benefiting_code, party_losing_code, weight
        )

        new_election = electopy.election(self.electoral_map, new_votes)

        return new_election

    def compare(self, comparison_election):
        """Compare two elections.

        This function still needs to be done.

        """

        original_election = election(self.electoral_map, self.votes)

        electopy.compare(original_election, comparison_election)


def _new_result(votes, party_benefiting_code, party_losing_code, weight=1.0):
    """Calculate the new voting results.

    Returns the transformation of votes, to a new result were a share (weight) of votes
    form party_losing goes to party_benefiting.

    Parameters
    ----------
    votes: DataFrame
        Votes per region per party in the election result.
    party_benefiting: int
        Code of the political party which gets a positive influx of votes.
    party_losing: int
        Code of the political party which gets a negative influx of votes.
    weight: float
        Share of votes from the losing party which goes to the benefiting party.

    Returns
    -------
    votes: DataFrame
        New votes per region per party in the election result.

    """

    votes[party_benefiting_code] = (
        votes[party_benefiting_code] + votes[party_losing_code] * weight
    )
    votes[party_losing_code] = votes[party_losing_code] * (1 - weight)

    return votes


def _most_voted_party(votes_per_party):
    """Calculate the most voted party.

    Given the number of votes per party in a region, calculates which is the most voted
    political party.

    Parameters
    ----------
    votes_per_party: Series
        The number of votes each political party got in a region.

    Returns
    -------
    party_with_most_votes: int
        Code of the political party with the largest number of votes.

    """

    party_with_most_votes = votes_per_party.sort_values(ascending=False).index[0]

    return party_with_most_votes


## cSpell: ignore astype D'Hondt
