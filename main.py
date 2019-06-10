import pandas as pd
import numpy as np
import random

import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import ListedColormap

import geopandas as gpd
import shapely

# Add Data

## Provincias

provincia=['A Coruna','Alava','Albacete','Alicante','Almeria','Asturias','Avila','Badajoz','Barcelona','Bizkaia','Burgos','Caceres','Cadiz','Cantabria','Castellon','Ceuta','Ciudad Real','Cordoba','Cuenca','Gipuzkoa','Girona','Granada','Guadalajara','Huelva','Huesca','Illes Balears','Jaen','La Rioja','Las Palmas','Leon','Lleida','Lugo','Madrid','Malaga','Melilla','Murcia','Navarra','Oursense','Palencia','Pontevedra','Salamanca','Segovia','Sevilla','Soria','Tarragona','Tenerife','Teruel','Toledo','Valencia','Valladolid','Zamora','Zaragoza']

## Resultados

Resultado={}
for prov in provincia:
    Resultado[prov]=pd.read_csv('Resultados/'+prov+'.csv',index_col=[0],usecols=['Candidaturas','Votos'])

## Escaños

Diputados={'A Coruna': 8,'Alava': 4,'Albacete': 4,'Alicante': 12,'Almeria': 6,'Asturias': 7,'Avila': 3,'Badajoz': 6,'Barcelona': 32,'Bizkaia': 8,'Burgos': 4,'Caceres': 4,'Cadiz': 9,'Cantabria': 5,'Castellon': 5,'Ceuta': 1,'Ciudad Real': 5,'Cordoba': 6,'Cuenca': 3,'Gipuzkoa': 6,'Girona': 6,'Granada': 7,'Guadalajara': 3,'Huelva': 5,'Huesca': 3,'Illes Balears': 8,'Jaen': 5,'La Rioja': 4,'Las Palmas': 8,'Leon': 4,'Lleida': 4,'Lugo': 4,'Madrid': 37,'Malaga': 11,'Melilla': 1,'Murcia': 10,'Navarra': 5,'Oursense': 4,'Palencia': 3,'Pontevedra': 7,'Salamanca': 4,'Segovia': 3,'Sevilla': 12,'Soria': 2,'Tarragona': 6,'Tenerife': 7,'Teruel': 3,'Toledo': 6,'Valencia': 15,'Valladolid': 5,'Zamora': 3,'Zaragoza': 7}

# Funciones

## Calculador de Escaños

def CalcularDiputados(Res,Dips):
    div=np.array([1/i for i in range(1,Dips+1)])
    df=Res['Votos'].apply(lambda x: x*div).apply(pd.Series).unstack().sort_values(ascending=False)[:Dips]
    x=df.index.get_level_values(1).value_counts()
    return x

## Calculador Parlamento

### Indice Partidos

def Partidos(Res):
    ind=pd.Index(['PP'])
    for prov in Res:
        ind=ind.union(Res[prov].index)
    return ind

### Composicion Parlmanetaria

def Parlamento(Res):
    Part=Partidos(Res)
    df=pd.DataFrame(data=Res,index=Part,dtype=int).replace(np.nan,0)
    return df.assign(Total=df.sum(axis=1))

## Partido mas Votado

def MasVotado(Res,provincia):
    df=pd.DataFrame(data=provincia,index=provincia)
    for prov in provincia:
        df.loc[prov]=Res[prov].sort_values(by='Votos',ascending=False).index[0]
    return df

## Elecciones

def Elecciones(Provincia, Votos, Dip):
    
    Elecciones={}
    ResDip={}
    for prov in Provincia:
        ResDip[prov]=CalcularDiputados(Votos[prov],Diputados[prov])
        
    Elecciones['Parlamento']=Parlamento(ResDip)
    Elecciones['Circunscripcion']=MasVotado(Votos,Provincia)
    Elecciones['Votos']=Votos
    
    return Elecciones

# Visualizacion

## Mapa

### Diccionario Nombres
def DicNombres():
    
    mapdict={
    'CÃ¡ceres': 'Caceres',
    'LÃ©rida': 'Lleida',
    'Gerona': 'Girona',
    'Orense': 'Oursense',
    'CÃ¡diz': 'Cadiz',
    'CastellÃ³n': 'Castellon',
    'AlmerÃ­a': 'Almeria',
    'MÃ¡laga': 'Malaga',
    'La CoruÃ±a': 'A Coruna',
    'Santa Cruz de Tenerife': 'Tenerife',
    'Baleares': 'Illes Balears',
    'Ãlava': 'Alava',
    'LeÃ³n': 'Leon',
    'Ãvila': 'Avila',
    'CÃ³rdoba': 'Cordoba',
    'JaÃ©n': 'Jaen'
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

def Mapa(Res,text=''):
    
    map_df=gpd.read_file('Map/ne_10m_admin_1_states_provinces.shp')
    spa=map_df.loc[map_df['iso_a2']=='ES']
    
    esp=MoverCanarias(spa)
    
    mapdict=DicNombres()
    
    esp['prov']=esp['name'].replace(mapdict)
    
    merge=esp.set_index('prov').join(Res['Circunscripcion'])
    
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
        'Podemos': '#6A2E68',
        'VOX': '#5AC035',
        'ERC': '#F3B217',
        'JxCAT': '#C40048',
        'PNV': '#009526',
        'EH Bildu': '#A3C940',
        'NA+': '#FFDA1A',
        'CC': '#E51C13',
        'PRC': '#DB6426',
        'COMPROMÍS': '#BECD48'
    }
    
    return Partidos.map(PartyColors).values

### Composicion

def Composicion(Res,text=''):
    
    sortedparl=Res['Parlamento'].Total.sort_values(ascending=False)
    
    label=CreateLabels(sortedparl)
    
    colors=CreateColors(sortedparl.index)
    
    plt.rcParams.update({'font.size':12})

    plt.figure(figsize=(10,10))
    plt.pie(sortedparl,colors=colors,wedgeprops=dict(width=0.5),startangle=90,labels=label,autopct=lambda x: disp(x),pctdistance=0.75,textprops={'fontsize':'large','weight':'bold'})
    plt.title('Composicion del Parlamento'+text,fontdict={'fontsize':32})
    plt.show()

# Cambio Electoral

## Nuevo Resultado

def NuevoResultado(Res,Part1,Part2,Peso=1):
    NRes=Res.copy()
    if np.isin('NA+',NRes.index) & ((Part1=='PP') | (Part1=='Cs')):
        Part1='NA+'
    if np.isin(Part1,NRes.index) & np.isin(Part2,NRes.index):
        NRes.loc[Part1]=NRes.loc[Part1]+(NRes.loc[Part2]*Peso)
        NRes.loc[Part2]=NRes.loc[Part2]*(1-Peso)
    return NRes

## Nuevas Elecciones

def NuevasElecciones(Provincia, Votos, Diputados, Partido1, Partido2, Peso=1):
    
    NVotos={}
    NVotos['Partido1']=Partido1
    NVotos['Partido2']=Partido2
    NVotos['Peso']=Peso
    for prov in Provincia:
        NVotos[prov]=NuevoResultado(Votos[prov],Partido1, Partido2, Peso)
    
    return Elecciones(Provincia, NVotos, Diputados)

# Diferencia

def Diferencia(Res,NRes):
    
    Opc1=Res['Parlamento'].Total.sort_values(ascending=False)
    Opc2=NRes['Parlamento'].Total.sort_values(ascending=False)
    
    Partido1=NRes['Votos']['Partido1']
    Partido2=NRes['Votos']['Partido2']
    Peso=NRes['Votos']['Peso']
    
    DCH=['PP','VOX','Cs']
    IZQ=['PSOE','Podemos']
    
    Newid=Opc1.index.intersection(Opc2.index)
    
    colors=CreateColors(Newid)
    
    dif=Opc2-Opc1
    order=abs(dif.loc[(dif!=0) & dif.notna()]).sort_values(ascending=False)
    
    fig, ax=plt.subplots()

    plt.rcParams.update({'font.size':32})
    
    ind=np.arange(len(Newid))
    width=0.35
    fig.set_size_inches(31,19)
    
    locP1=ind[Newid==Partido1][0]
    
    p1 = ax.bar(ind,Opc1[Newid],width,color=colors)
    p2 = ax.bar(ind+width,Opc2[Newid],width,color=colors,alpha=0.5)
    
    if NRes['Votos']['Peso']==1:
        dif.loc[Partido1]=dif.loc[Partido1]-Opc1.loc[Partido2]
        Miss=Opc1.index.difference(Newid)
        color1=CreateColors(Miss)
        p3 = ax.bar(locP1,Opc1[Miss],width,color=color1,bottom=Opc1.iloc[locP1])
        ax.legend((p1[locP1],p2[locP1]),('{0:s} y {1:s} Separados'.format(Partido1,Partido2),'{0:s} + {1:s}'.format(Partido1,Partido2)))
    else:
        ax.legend((p1[locP1],p2[locP1]),('{0:s} y {1:s} Separados'.format(Partido1,Partido2),'{0:s} + {2:2.0f}% {1:s}'.format(Partido1,Partido2,Peso*100)))
    
    order=abs(dif.loc[(dif!=0) & dif.notna()]).sort_values(ascending=False)
    
    ax.set_title('Resultado de las elecciones si el {2:2.0f}% del voto de {1:s} fuera al {0:s}'.format(Partido1,Partido2,Peso*100))
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(Newid)
    
    ax.text(6,60,u'Diferencia:\n\n'+'\n'.join('{:10s}{:+.0f}'.format(i,dif.loc[i]) for i in order.index),family='monospace')
    ax.text(9,60,u'Bloque Derecha:   {:+.0f}\nBloque Izquierda: {:+.0f}'.format(dif.loc[dif.index.isin(DCH)].sum(),dif.loc[dif.index.isin(IZQ)].sum()),family='monospace')
    for i in ind:
        ax.text(i+width*0.6,Opc2[Newid[i]]+5,'{:.0f}'.format(Opc2[Newid[i]]))
    plt.show()

# Procedural Test

Res1=Elecciones(provincia, Resultado, Diputados)
Res2=NuevasElecciones(provincia, Resultado, Diputados, 'PP', 'VOX',1)
Mapa(Res2)
Composicion(Res2)
Diferencia(Res1,Res2)