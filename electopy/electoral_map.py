class electoral_map:

    def __init__ (self,parties,regions,distribution):

        self.parties = parties
        self.regions = regions
        self.distribution = distribution

        self.total_mps = self.sum_mps(self.distribution)

    def sum_mps(self,distribution):

        total = distribution.sum()

        return total