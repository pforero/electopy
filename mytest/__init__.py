import pandas as pd
import electopy


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

    Res1=electopy.Elecciones(votos,diputados)
    Res2=electopy.NuevasElecciones(votos,diputados,'PP','PSOE', partidos, 1)
    electopy.Mapa(Res1,provincias)
    electopy.Composicion(Res2, partidos)

## ZIP Test

def ziptest():

    # Cargar Elecciones

    df=electopy.CargarElecciones()
    partidos, provincias, votos, diputados = electopy.LimpiarDF(df) 

    # Test

    Res1=electopy.Elecciones(votos,diputados)
    Res2=electopy.NuevasElecciones(votos,diputados,'PP','PSOE', partidos, 1)
    electopy.Mapa(Res1,provincias)
    electopy.Composicion(Res2, partidos)