import electopy
import electopy.display
import electopy.electoral_map

import pandas as pd
import numpy as np

from matplotlib.colors import ListedColormap


class election:
    def __init__(self, electoral_map, votes):

        if not isinstance(electoral_map, electopy.electoral_map.electoral_map):

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

        mps_per_region = self.votes.apply(
            lambda votes_per_region: self.mps(votes_per_region.name), axis=1
        ).replace(np.nan, 0)

        total_mps = mps_per_region.sum().astype(int)

        return total_mps

    def most_voted(self):

        most_voted = self.votes.apply(most_voted_party, axis=1)

        return most_voted

    def spain_map(self, canary_x=7, canary_y=5, text=""):

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

        sorted_parlament = self.parlament().sort_values(ascending=False)

        labels = electopy.display.create_parlament_labels(
            sorted_parlament.rename(self.parties)
        )

        colors = electopy.display.create_colors(
            sorted_parlament.rename(self.parties).index
        )

        electopy.display.create_parlament_plot(sorted_parlament, colors, labels, text)

    def transform(self, party_benefiting, party_losing, weight=1):

        # Needs to find a new way to do (and store parameters) transformations

        party_benefiting_code = self.parties[self.parties == party_benefiting].index[0]
        party_losing_code = self.parties[self.parties == party_losing].index[0]

        new_votes = new_result(
            self.votes.copy(), party_benefiting_code, party_losing_code, weight
        )

        new_election = electopy.election(self.electoral_map, new_votes)

        return new_election

    def compare(self, comparison_election):

        original_election = election(self.electoral_map, self.votes)

        electopy.compare(original_election, comparison_election)


######################################### Helper Functions ######################################################################


def new_result(votes, party_benefiting_code, party_losing_code, weight=1):

    votes[party_benefiting_code] = (
        votes[party_benefiting_code] + votes[party_losing_code] * weight
    )
    votes[party_losing_code] = votes[party_losing_code] * (1 - weight)

    return votes


def most_voted_party(votes_per_party):

    return votes_per_party.sort_values(ascending=False).index[0]


## cSpell: ignore astype
