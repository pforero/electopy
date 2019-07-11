# cSpell: disable

import pandas as pd

import urllib.request
import zipfile


def get_mir_dictionary():

    election_mir_dictionary = {
        2016: "PROV_02_201606_1.zip",
        2015: "PROV_02_201512_1.zip",
        2011: "PROV_02_201111_1.zip",
        2008: "PROV_02_200803_1.zip",
        2004: "PROV_02_200403_1.zip",
        2000: "PROV_02_200003_1.zip",
        1996: "PROV_02_199603_1.zip",
        1993: "PROV_02_199306_1.zip",
        1989: "PROV_02_198910_1.zip",
        1986: "PROV_02_198606_1.zip",
        1982: "PROV_02_198210_1.zip",
        1979: "PROV_02_197903_1.zip",
        1977: "PROV_02_197706_1.zip",
    }

    return election_mir_dictionary


def get_file_name(year=2016):

    mir_dictionary = get_mir_dictionary()

    try:

        file_name = mir_dictionary[year]

    except:

        print("Can not find the year of the election. 2016 will be loaded")

        file_name = mir_dictionary[2016]

    return file_name


def download_election(year=2016, save_folder="past_elections"):

    mir_address = "http://www.infoelectoral.mir.es/infoelectoral/docxl/"
    file_name = get_file_name(year)

    url = mir_address + file_name
    save_location = save_folder + "/" + file_name

    urllib.request.urlretrieve(url, save_location)


def file_to_df(file_name):

    if file_name.endswith(".zip"):

        excel_file_name = file_name.rsplit("/")[-1][:-4] + ".xlsx"
        archive = zipfile.ZipFile(file_name, "r")
        excel_file = archive.open(excel_file_name)

    else:

        excel_file = file_name

    # nrows=54 works because the number of regions is the same for all elections. If there were any changes it wouldn't work

    election_dataframe = pd.read_excel(excel_file, skiprows=range(3), nrows=54)

    return election_dataframe


def load_election(file_name=None, year=2016, save_folder="past_elections"):

    if file_name:

        try:

            file_to_df(file_name)

        except:

            print("File Not Found!")
    else:

        file_name = save_folder + "/" + get_file_name(year)

        try:

            election_dataframe = file_to_df(file_name)

        except:

            download_election(year=year, save_folder=save_folder)

            election_dataframe = file_to_df(file_name)

        return election_dataframe


def get_parties(df):

    parties = df.loc[0, (df.loc[1] == "Votos")].str.strip()

    parties.index = range(len(parties))
    parties.name = "Parties"

    return parties


def get_voting_regions(df):

    col_name = df.columns[df.loc[1] == "Nombre de Provincia"]
    col_code = df.columns[df.loc[1] == "Código de Provincia"]

    regions = df.loc[2:, col_name].iloc[:, 0].str.strip()
    regions.index = df.loc[2:, col_code].iloc[:, 0]

    regions.index.name = None
    regions.name = "Provincias"

    return regions


def get_votes(df):

    parties = get_parties(df)
    col_code = df.columns[df.loc[1] == "Código de Provincia"]

    votes = df.loc[2:, (df.loc[1] == "Votos")]
    votes.columns = parties.index

    votes = votes.set_index(df.loc[2:, col_code].values.squeeze())

    return votes


def get_mps(df):

    parties = get_parties(df)
    col_code = df.columns[df.loc[1] == "Código de Provincia"]

    mps = df.loc[2:, (df.loc[1] == "Diputados")]
    mps.columns = parties.index

    mps = mps.set_index(df.loc[2:, col_code].values.squeeze())

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


def clean_df(votes, distribution):

    regions = pd.Series(data=range(len(votes.index)), index=votes.index)
    votes.rename(regions, inplace=True)
    distribution.rename(regions, inplace=True)
    regions = pd.Series(data=regions.index.str.strip(), index=regions)

    parties = pd.Series(data=range(len(votes.columns)), index=votes.columns)
    votes.rename(columns=parties, inplace=True)
    parties = pd.Series(data=parties.index.str.strip(), index=parties)

    return parties, regions, votes, distribution
