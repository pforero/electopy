import electopy.display

import numpy as np

from matplotlib import cm
from matplotlib.colors import to_hex

import shapely

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

## Mover Canarias

def move_canary(geo,x=7,y=5):
    
    geo.loc[Geo['adm0_sr']==3,'geometry']=geo.loc[geo['adm0_sr']==3,'geometry'].apply(lambda n: shapely.affinity.translate(n,xoff=x,yoff=y))
    
    return geo

def create_labels(parl,limit=6):
    
    label=list(parl.index)
    
    for i,v in enumerate(label):

        if parl[v]<limit:

            label[i]=''
    
    return label

def display(pct):

    if pct>1.5:

        return '{:.0f}'.format(pct*3.5)

def create_colors(parties):
    
    partycolors = party_colors()

    colormap = np.vectorize(partycolors.get)(parties)
    
    missing = np.sum(colormap=='None')

    if missing>10:

        extracolors = cm.get_cmap('tab20',20)(np.linspace(0,1,20))

    else: 
            
        extracolors = cm.get_cmap('tab10',10)(np.linspace(0,1,10)) 

    i = 0
    cmap=[]

    for party in parties:

        try: 
                    
                c = partycolors[party]

        except:

                c = extracolors[i]
                i += 1

        cmap.append(c)
    
    return cmap

def party_colors():
    
    pc={
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

    return pc