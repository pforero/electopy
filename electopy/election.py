class election:

    def __init__(self,em,votes):

        if not isinstance(em,electoral_map):

            raise('Not and Electoral Map')

        self.em = em
        self.votes = votes

        self.parties = em.parties
        self.regions = em.regions
        self.distribution = em.distribution