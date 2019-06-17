import electopy
import electopy.display
from electopy.electoral_map import electoral_map

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import geopandas as gpd

class election:

    def __init__(self,em,votes):

        # Need a way to check that the coding for parties/regions match the index and columns of votes

        if not isinstance(em,electoral_map):

            raise ValueError('Not an Electoral Map: em is not of class electoral_map')

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

        mas_vot = self.votes.apply(lambda x: x.sort_values(ascending=False).index[0],axis=1)

        return mas_vot

    def spain_map(self, text=''):

        # This file should either be downloaded or done in some way where the location of the folder doesn't matter

        # Most of this should be divided into sub functions for easier readability

        map_df=gpd.read_file('map/ne_10m_admin_1_states_provinces.shp')
        spa=map_df.loc[map_df['iso_a2']=='ES']

        esp=electopy.display.move_canary(spa)

        mapdict=electopy.display.correct_region_names()

        # This line brings out a slicing warrning. Find a better way fo doing it that does not bring a warning
        esp['prov']=esp['name'].replace(mapdict)

        merge=esp.set_index('prov').join(pd.DataFrame(data=self.most_voted().values,index=self.most_voted().index.map(self.regions)))

        colormap=electopy.display.color_map()

        # Nicer formatting needed. Map colours need to match political parties. Parties names need to be names, not codes

        plt.rcParams.update({'font.size':32})

        ax=merge.plot(column=0,cmap=colormap,figsize=(31,19),linewidth=0.8,edgecolor='0.8',legend=True,categorical=True)
        ax.set_axis_off()
        ax.set_title('Ganador por Circunscripcion'+text)
        plt.show()

    def parlament_composition(self, text=''):

        sortedparl=self.parlament().sort_values(ascending=False)

        label=electopy.display.create_labels(sortedparl.rename(self.parties))

        colors=electopy.display.create_colors(sortedparl.rename(self.parties).index)

        plt.rcParams.update({'font.size':12})

        plt.figure(figsize=(10,10))
        plt.pie(sortedparl,wedgeprops=dict(width=0.5),startangle=90,labels=label,autopct=lambda x: electopy.display.disp(x),pctdistance=0.75,textprops={'fontsize':'large','weight':'bold'})
        plt.title('Composicion del Parlamento'+text,fontdict={'fontsize':32})
        plt.show()

    def transform(self, party1, party2, weight=1):

        # Needs to find a new way to do (and store parameters) transformations
        # Use party names, not party codes

        new_votes=new_result(self.votes, party1 ,party2 ,weight)

        new_election=electopy.election(self.em,new_votes)

        return new_election

    def compare(self, el2):

        el = election(self.em,self.votes)

        electopy.compare(el, el2)

######################################### Helper Functions ######################################################################

def new_result(votes,party1,party2,weight=1):
    
    votes[party1]=votes[party1]+votes[party2]*weight
    votes[party2]=votes[party2]*(1-weight)
    
    return votes
