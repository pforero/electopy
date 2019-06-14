class electoral_map:

    def __init__ (self,parties,regions,distribution):

        self.parties = parties
        self.regions = regions
        self.distribution = distribution

        self.total_mps = sum_mps(distribution)

##################################### Helper Functions #######################################

def sum_mps(distribution):

    total = distribution.sum()

    return total