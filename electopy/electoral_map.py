class electoral_map:
    def __init__(self, parties, regions, distribution):

        if not regions.index.equals(distribution.index):

            raise ValueError("Index of regions do not match the index of distribution")

        self.parties = parties
        self.regions = regions
        self.distribution = distribution

        self.total_mps = _sum_mps(distribution)


##################################### Helper Functions #######################################


def _sum_mps(distribution):

    total = distribution.sum()

    return total
