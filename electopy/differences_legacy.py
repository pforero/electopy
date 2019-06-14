import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import ListedColormap

import geopandas as gpd
import shapely

import urllib.request
import zipfile

############################################ Diferencia (Legacy) ##############################################################
# Lo dejo como referencia. Pero hasta no crear todo nuevo, esto es demasiado complejo para tocarlo cada vez que cambiamos algo

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