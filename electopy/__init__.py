import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import ListedColormap

import geopandas as gpd
import shapely

import urllib.request
import zipfile

def MIR():
    
    past_elections={2016:'PROV_02_201606_1.zip'}
    
    return past_elections

def GetFileName(year=2016):
    
    past_elections=MIR()
    
    try:
        filename=past_elections[year]
    except:
        filename=past_elections[2016]
        
    return filename

def DescargarElecciones(year=2016,save_folder='past_elections'):
    
    miraddress='http://www.infoelectoral.mir.es/infoelectoral/docxl/'
    filename=GetFileName(year)
        
    url=miraddress+filename
    location=save_folder+'/'+filename
    urllib.request.urlretrieve(url, location)

def GetFile_as_DF(file_name):
    
    if file_name.endswith('.zip'):
        
        end_file=file_name.rsplit('/')[-1][:-4]+'.xlsx'
        archive = zipfile.ZipFile(file_name,'r')
        xlsxfile = archive.open(end_file)
        
    else:
        
        xlsxfile = file_name
        
    return pd.read_excel(xlsxfile,skiprows=range(3))

def CargarElecciones(file_name=None,year=2016,save_folder='past_elections'):
    
    if file_name:
        
        try:
            
            GetFile_as_DF(file_name)
            
        except:
            
            print('File Not Found!')
    else:
        
        past_elections=MIR()
        file_name=save_folder+'/'+GetFileName(year)
        
        try:
            
            df=GetFile_as_DF(file_name)
            
        except:
            
            DescargarElecciones(year=year,save_folder=save_folder)
            df=GetFile_as_DF(file_name)
            
    return df

def LimpiarPartidos(df):
    
    Partidos=df.loc[0,(df.loc[1]=='Votos')].str.strip()
    Partidos.index=range(len(Partidos))
    Partidos.name='Partidos'
    
    return Partidos

def LimpiarProvincias(df):
    
    colNombre=df.columns[df.loc[1]=='Nombre de Provincia']
    colCodigo=df.columns[df.loc[1]=='Código de Provincia']
    
    prov=df.loc[2:,colNombre].iloc[:,0].str.strip()
    prov.index=df.loc[2:,colCodigo].iloc[:,0]
    prov.index.name=None
    
    Provincias=prov
    Provincias.name='Provincias'
    
    return Provincias

def LimpiarVotos(df):
    
    Partidos=LimpiarPartidos(df)
    colCodigo=df.columns[df.loc[1]=='Código de Provincia']
    
    Votos=df.loc[2:,(df.loc[1]=='Votos')]
    Votos.columns=Partidos.index

    Votos=Votos.set_index(df.loc[2:,colCodigo].values.squeeze())
    
    return Votos

def LimpiarDiputados(df):
    
    Partidos=LimpiarPartidos(df)
    colCodigo=df.columns[df.loc[1]=='Código de Provincia']
    
    Votos=df.loc[2:,(df.loc[1]=='Diputados')]
    Votos.columns=Partidos.index
    
    Votos=Votos.set_index(df.loc[2:,colCodigo].values.squeeze())
    
    return Votos

def DistribucionEscanos(diputados):
    
    escanos = diputados.sum(axis=1)
    
    return escanos.astype(int)

def LimpiarDF(df):
    
    partidos = LimpiarPartidos(df)
    provincias = LimpiarProvincias(df)
    votos = LimpiarVotos(df)
    diputados = LimpiarDiputados(df)
    escanos = DistribucionEscanos(diputados)
    
    return partidos, provincias, votos, escanos

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
    
    map_df=gpd.read_file('Map/ne_10m_admin_1_states_provinces.shp')
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