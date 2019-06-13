import electopy.loading

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import ListedColormap

import geopandas as gpd
import shapely

import urllib.request
import zipfile

def from_mir(year=2016):

    df = electopy.loading.load_election(year)
    parties, regions, votes, distribution = electopy.loading.clean_df(df) 

    return parties, regions, votes, distribution

######################################################################################################################################################

# Funciones

## Calculador de Escaños

def CalcularDiputados(Res,Dips):
    
    div=np.array([1/i for i in range(1,Dips+1)])
    df=Res.apply(lambda x: x*div).apply(pd.Series).unstack().sort_values(ascending=False)[:Dips]
    x=df.index.get_level_values(1).value_counts()

    return x

## Composicion Parlmanetaria

def Parlamento(Votos,Dip):

    df=Votos.apply(lambda x: CalcularDiputados(x,Dip.loc[x.name]),axis=1).replace(np.nan,0)
    total=pd.DataFrame(data=df.sum(),columns=['Total'])

    return df.append(total.T)

## Partido mas Votado

def MasVotado(Votos):

    mas_vot=Votos.apply(lambda x: x.sort_values(ascending=False).index[0],axis=1)

    return mas_vot

## Elecciones

def Elecciones(Votos, Dip):
    
    Elecciones={}

    Elecciones['Parlamento']=Parlamento(Votos,Dip)
    Elecciones['Circunscripcion']=MasVotado(Votos)
    Elecciones['Votos']=Votos
    
    return Elecciones

# Visualizacion

## Mapa

### Diccionario Nombres
def DicNombres():
    
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

### Color Map

def CreateColorMap():
    
    colormap=cm.get_cmap('Blues',5)(np.linspace(0,1,5))
    
    colormap[0]=[243/256,178/256,23/256,1]
    colormap[1]=[201/256,28/256,41/256,1]
    colormap[2]=[0/256,149/256,38/256,1]
    colormap[3]=[0/256,85/256,167/256,1]
    colormap[4]=[237/256,28/256,36/256,1]
    
    return ListedColormap(colormap)

### Mover Canarias

def MoverCanarias(Geo,x=0,y=0):
    
    for i in Geo.loc[Geo['adm0_sr']==3].index:
        Geo['geometry'].loc[i]=shapely.affinity.translate(Geo['geometry'].loc[i], xoff=x, yoff=y)
    
    return Geo

### Mapa

def Mapa(Res, provincias, text=''):
    
    map_df=gpd.read_file('map/ne_10m_admin_1_states_provinces.shp')
    spa=map_df.loc[map_df['iso_a2']=='ES']
    
    esp=MoverCanarias(spa)
    
    mapdict=DicNombres()
    
    esp['prov']=esp['name'].replace(mapdict)
    
    merge=esp.set_index('prov').join(pd.DataFrame(data=Res['Circunscripcion'].values,index=Res['Circunscripcion'].index.map(provincias)))
    
    colormap=CreateColorMap()
    
    plt.rcParams.update({'font.size':32})

    ax=merge.plot(column=0,cmap=colormap,figsize=(31,19),linewidth=0.8,edgecolor='0.8',legend=True,categorical=True)
    ax.set_axis_off()
    ax.set_title('Ganador por Circunscripcion'+text)
    plt.show()

## Parlamento

### Create Labels

def CreateLabels(Parl,Limite=6):
    
    label=list(Parl.index)
    
    for i,v in enumerate(label):
        if Parl[v]<Limite:
            label[i]=''
    
    return label

### Display Escaños

def disp(pct):
    if pct>1.5:
        return '{:.0f}'.format(pct*3.5)

### Create Colors

def CreateColors(Partidos):
    
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

### Composicion

def Composicion(Res, partidos, text=''):
    
    sortedparl=Res['Parlamento'].loc['Total'].sort_values(ascending=False)
    
    label=CreateLabels(sortedparl.rename(partidos))
    
    colors=CreateColors(sortedparl.rename(partidos).index)
    
    plt.rcParams.update({'font.size':12})

    plt.figure(figsize=(10,10))
    plt.pie(sortedparl,colors=colors,wedgeprops=dict(width=0.5),startangle=90,labels=label,autopct=lambda x: disp(x),pctdistance=0.75,textprops={'fontsize':'large','weight':'bold'})
    plt.title('Composicion del Parlamento'+text,fontdict={'fontsize':32})
    plt.show()

# Cambio Electoral

## Nuevo Resultado

def NuevoResultado(Res,Part1,Part2,Peso=1):
    
    NRes=Res.copy()
    NRes[Part1]=NRes[Part1]+NRes[Part2]*Peso
    NRes[Part2]=NRes[Part2]*(1-Peso)
    
    return NRes

## Nuevas Elecciones

def NuevasElecciones(Votos, Diputados, Partido1, Partido2, partidos, Peso=1):
    
    NVotos={}
    NVotos['Partido1']=partidos[partidos==Partido1].index[0]
    NVotos['Partido2']=partidos[partidos==Partido2].index[0]
    NVotos['Peso']=Peso
    
    NVotos['Votos']=NuevoResultado(Votos,NVotos['Partido1'],NVotos['Partido2'],Peso)
    
    return Elecciones(NVotos['Votos'], Diputados)