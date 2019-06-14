import electopy
import electopy.electoral_map
import electopy.election
import pandas as pd

# CSV Test

def csvtest():

    votos=pd.read_csv('mytest/test_votos.csv',index_col=0,thousands=',')
    diputados=pd.read_csv('mytest/test_diputados.csv',squeeze=True,index_col=0)

    provincias=pd.Series(data=range(len(votos.index)),index=votos.index)
    votos.rename(provincias,inplace=True)
    diputados.rename(provincias,inplace=True)
    provincias=pd.Series(data=provincias.index.str.strip(),index=provincias)

    partidos=pd.Series(data=range(len(votos.columns)),index=votos.columns)
    votos.rename(columns=partidos,inplace=True)
    partidos=pd.Series(data=partidos.index.str.strip(),index=partidos)

    em = electopy.electoral_map.electoral_map(partidos,provincias,diputados)
    el = electopy.election.election(em,votos)
    el2 = el.transform(0,1)
    el.spain_map()
    el2.parlament_composition()

## ZIP Test

def ziptest():

    el = electopy.from_mir()
    el2 = el.transform(0,1)

    el.spain_map()
    el2.parlament_composition()
