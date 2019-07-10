import electopy
import electopy.display
from electopy.electoral_map import electoral_map

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class election:

    def __init__(self,em,votes):

        if not isinstance(em,electoral_map):

            raise ValueError('Not an Electoral Map: em is not of class electoral_map')

        if not votes.columns.equals(em.parties.index):

            raise ValueError('votes columns do not match the parties of the electoral map')

        if not votes.index.equals(em.regions.index):

            raise ValueError('votes index does not match the regions of the electoral map')

        self.em = em
        self.votes = votes

        self.parties = em.parties
        self.regions = em.regions
        self.distribution = em.distribution

    def mps(self,region):

        # This should allow you to chose for which parties and which regions you get the result
    
        div = np.array([1/i for i in range(1,self.distribution[region]+1)])

        df = self.votes.loc[region].apply(lambda x: x*div).apply(pd.Series).unstack().sort_values(ascending=False)[:self.distribution[region]]

        x = df.index.get_level_values(1).value_counts()

        # It should return ALL parties mps chosen, not just with those with a value > 0

        return x

    def parlament(self):

        df = self.votes.apply(lambda x: self.mps(x.name),axis=1).replace(np.nan,0)

        total = df.sum().astype(int)

        return total

    def most_voted(self):

        most_voted = self.votes.apply(lambda x: x.sort_values(ascending=False).index[0],axis=1)

        return most_voted

    def spain_map(self, canary_x=7, canary_y=5, text=''):

        esp = electopy.display.get_spain_map(x=canary_x, y=canary_y)

        esp = electopy.display.proper_names(esp)

        results = pd.DataFrame(data=self.most_voted().map(self.parties).values,index=self.most_voted().index.map(self.regions))

        merge = esp.join(results)

        colormap = ListedColormap(electopy.display.create_colors(self.most_voted().map(self.parties).sort_values().unique()))

        electopy.display.create_map_plot(merge,colormap,text)

    def parlament_composition(self, text=''):

        sortedparl=self.parlament().sort_values(ascending=False)

        label=electopy.display.create_parlament_labels(sortedparl.rename(self.parties))

        colors=electopy.display.create_colors(sortedparl.rename(self.parties).index)

        electopy.display.create_parlament_plot(sortedparl,colors,label,text)

    def transform(self, party1, party2, weight=1):

        # Needs to find a new way to do (and store parameters) transformations
        # Use party names, not party codes

        new_votes = new_result(self.votes, party1 ,party2 ,weight)

        new_election = electopy.election(self.em,new_votes)

        return new_election

    def compare(self, el2):

        el = election(self.em,self.votes)

        electopy.compare(el, el2)

######################################### Helper Functions ######################################################################

def new_result(votes,party1,party2,weight=1):
    
    votes[party1] = votes[party1]+votes[party2]*weight
    votes[party2] = votes[party2]*(1-weight)
    
    return votes
