import electopy.display

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import to_hex

import geopandas as gpd

import shapely

def get_spain_map(x=0,y=0):

    # This file should either be downloaded or done in some way where the location of the folder doesn't matter

    map_df = gpd.read_file('map/ne_10m_admin_1_states_provinces.shp')
    spa = map_df.loc[map_df['iso_a2']=='ES'].copy()

    esp = electopy.display.move_canary(spa, x=x, y=y)

    return esp

def move_canary(geo,x=0,y=0):
    
    geo.loc[geo['adm0_sr']==3,'geometry'] = geo.loc[geo['adm0_sr']==3,'geometry'].apply(lambda n: shapely.affinity.translate(n, xoff=x, yoff=y))
    
    return geo

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

def proper_names(esp):

    mapdict = electopy.display.correct_region_names()

    esp = esp.assign(prov = esp['name'].replace(mapdict))

    return esp.set_index('prov')

def create_parlament_labels(parl,limit=6):
    
    label=list(parl.index)
    
    for i,v in enumerate(label):

        if parl[v]<limit:

            label[i]=''
    
    return label

def display(pct):

    if pct>1.5:

        return '{:.0f}'.format(pct*3.5)

def create_parlament_colors(parties):
    
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

def create_map_plot(merge,colormap,text):

    ax = merge.plot(column=0, cmap=colormap, linewidth=0.8, edgecolor='0.8', legend=True, categorical=True)
    ax.set_axis_off()
    ax.set_title('Winner by region: '+text)

    plt.show()

def create_parlament_plot(sortedparl,colors,label,text):

    plt.pie(sortedparl,colors=colors,wedgeprops=dict(width=0.5),startangle=90,labels=label,autopct=lambda x: electopy.display.display(x),pctdistance=0.75,textprops={'fontsize':'large','weight':'bold'})
    plt.title('Composicion del Parlamento: '+text,fontdict={'fontsize':32})
    plt.show()