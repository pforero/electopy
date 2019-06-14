import electopy.display

import numpy as np

from matplotlib import cm
from matplotlib.colors import ListedColormap

import shapely

# Mapa

## Diccionario Nombres
def correct_region_names():
    
    mapdict={
    'CÃ¡ceres': 'Cáceres',
    'Orense': 'Ourense',
    'CÃ¡diz': 'Cádiz',
    'CastellÃ³n': 'Castellón / Castelló',
    'AlmerÃ­a': 'Almería',
    'MÃ¡laga': 'Málaga',
    'La CoruÃ±a': 'A Coruña',
    'Ãlava': 'Araba - Álava',
    'LeÃ³n': 'León',
    'Ãvila': 'Ávila',
    'CÃ³rdoba': 'Córdoba',
    'JaÃ©n': 'Jaén',
    'Alicante': 'Alicante / Alacant',
    'Valencia':'Valencia / València',
    'Baleares': 'Illes Balears',
    'Gerona': 'Girona',
    'LÃ©rida': 'Lleida'
    }
    
    return mapdict

## Color Map

def color_map():
    
    colormap=cm.get_cmap('Blues',5)(np.linspace(0,1,5))
    
    colormap[0]=[243/256,178/256,23/256,1]
    colormap[1]=[201/256,28/256,41/256,1]
    colormap[2]=[0/256,149/256,38/256,1]
    colormap[3]=[0/256,85/256,167/256,1]
    colormap[4]=[237/256,28/256,36/256,1]
    
    return ListedColormap(colormap)

## Mover Canarias

def move_canary(Geo,x=0,y=0):

    # This function currently brings out a warning. Find a better way to do it without warnings
    
    for i in Geo.loc[Geo['adm0_sr']==3].index:
        Geo['geometry'].loc[i]=shapely.affinity.translate(Geo['geometry'].loc[i], xoff=x, yoff=y)
    
    return Geo

# Parlamento

## Create Labels

def create_labels(Parl,Limite=6):
    
    label=list(Parl.index)
    
    for i,v in enumerate(label):
        if Parl[v]<Limite:
            label[i]=''
    
    return label

## Display Escaños

def disp(pct):
    if pct>1.5:
        return '{:.0f}'.format(pct*3.5)

## Create Colors

def create_colors(Partidos):
    
    PartyColors={
        'PSOE':'#ED1C24',
        'PP': '#0055A7',
        'Cs': '#FA5000',
        "C's": '#FA5000',
        'Podemos': '#6A2E68',
        'PODEMOS-IU-EQUO': '#6A2E68',
        'ECP': '#6A2E68',
        'PODEMOS-EN MAREA-ANOVA-EU': '#6A2E68',
        'VOX': '#5AC035',
        'ERC': '#F3B217',
        'ERC-CATSÍ': '#F3B217',
        'CDC': '#C40048',
        'JxCAT': '#C40048',
        'PNV': '#009526',
        'EAJ-PNV': '#009526',
        'EH Bildu': '#A3C940',
        'NA+': '#FFDA1A',
        'CC': '#E51C13',
        'CCa-PNC': '#E51C13',
        'PRC': '#DB6426',
        'COMPROMÍS': '#BECD48',
        'PODEMOS-COMPROMÍS-EUPV': '#BECD48',
    }
    
    return Partidos.map(PartyColors).values