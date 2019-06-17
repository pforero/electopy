import electopy
import electopy.electoral_map
import electopy.election
import pandas as pd

# CSV Test

def csvtest():

    votos=pd.read_csv('mytest/test_votos.csv',index_col=0,thousands=',')
    diputados=pd.read_csv('mytest/test_diputados.csv',squeeze=True,index_col=0)

    el = electopy.from_df(votos,diputados)
    el2 = el.transform(0,1)

    el.spain_map()
    el2.parlament_composition()

## ZIP Test

def ziptest(year=2016):

    el = electopy.from_mir(year)
    el2 = el.transform(0,1)

    el.spain_map()
    el2.parlament_composition()
