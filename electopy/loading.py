import pandas as pd

import urllib.request
import zipfile


def mir_dict():
    
    election_dictionary = {2016:'PROV_02_201606_1.zip'}
    
    return election_dictionary

def get_file_name(year=2016):
    
    mir_dictionary = mir_dict()
    
    try:

        filename=mir_dictionary[year]

    except:

        print('Can not find the year of the election. 2016 will be loaded')

        filename = mir_dictionary[2016]
        
    return filename

def download_election(year=2016,save_folder='past_elections'):
    
    miraddress = 'http://www.infoelectoral.mir.es/infoelectoral/docxl/'
    filename = get_file_name(year)
        
    url = miraddress+filename
    location = save_folder+'/'+filename

    urllib.request.urlretrieve(url, location)

def file_to_df(file_name):
    
    if file_name.endswith('.zip'):
        
        end_file = file_name.rsplit('/')[-1][:-4]+'.xlsx'
        archive =  zipfile.ZipFile(file_name,'r')
        excel_file =  archive.open(end_file)
        
    else:
        
        excel_file = file_name
        
    df = pd.read_excel(excel_file,skiprows=range(3))

    return df

def load_election(file_name=None,year=2016,save_folder='past_elections'):
    
    if file_name:
        
        try:
            
            file_to_df(file_name)
            
        except:
            
            print('File Not Found!')
    else:
        
        file_name = save_folder+'/'+get_file_name(year)
        
        try:
            
            df = file_to_df(file_name)
            
        except:
            
            download_election(year=year,save_folder=save_folder)

            df = file_to_df(file_name)
            
        return df

def get_parties(df):
    
    parties = df.loc[0,(df.loc[1]=='Votos')].str.strip()

    parties.index = range(len(parties))
    parties.name = 'Parties'
    
    return parties

def get_voting_regions(df):
    
    col_name = df.columns[df.loc[1]=='Nombre de Provincia']
    col_code = df.columns[df.loc[1]=='Código de Provincia']
    
    regions = df.loc[2:,col_name].iloc[:,0].str.strip()
    regions.index = df.loc[2:,col_code].iloc[:,0]
    
    regions.index.name = None
    regions.name = 'Provincias'
    
    return regions

def get_votes(df):
    
    parties = get_parties(df)
    col_code = df.columns[df.loc[1]=='Código de Provincia']
    
    votes = df.loc[2:,(df.loc[1]=='Votos')]
    votes.columns = parties.index

    votes = votes.set_index(df.loc[2:,col_code].values.squeeze())
    
    return votes

def get_mps(df):
    
    parties = get_parties(df)
    col_code = df.columns[df.loc[1]=='Código de Provincia']
    
    mps = df.loc[2:,(df.loc[1]=='Diputados')]
    mps.columns = parties.index
    
    mps = mps.set_index(df.loc[2:,col_code].values.squeeze())
    
    return mps

def distribution_of_mps(mps):
    
    distribution = mps.sum(axis=1).astype(int)
    
    return distribution

def clean_mir(df):
    
    parties = get_parties(df)
    regions = get_voting_regions(df)
    votes = get_votes(df)
    mps = get_mps(df)
    distribution = distribution_of_mps(mps)
    
    return parties, regions, votes, distribution

def clean_df(votes,distribution):

    regions = pd.Series(data=range(len(votes.index)),index=votes.index)
    votes.rename(regions,inplace=True)
    distribution.rename(regions,inplace=True)
    regions = pd.Series(data=regions.index.str.strip(),index=regions)

    parties = pd.Series(data=range(len(votes.columns)),index=votes.columns)
    votes.rename(columns=parties,inplace=True)
    parties = pd.Series(data=parties.index.str.strip(),index=parties)

    return parties, regions, votes, distribution