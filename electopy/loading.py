"""Electopy.loading

This module contains functions that help to load election results, both from the
Ministry's of Interior (MIR) webpage or from a custom dataframe, and clean those results
into the format used by electopy to create electoral_maps and elections.

"""

import pandas as pd

import urllib.request
import zipfile


def load_election(file_name=None, year=2016, save_folder="past_elections"):
    """Load the election results as a dataframe with the MIR's format.

    The results are loaded, either providing directly the name of the file, or the year
    of the election and the folder it is saved, if it comes from the MIR's webpage.

    If a file_name is provided, it would look directly for the file name. Else, it will
    look for the year's election in  the save_folder.

    Parameters
    ----------
    file_name: str
        Name of the zip/excel file with the election results.
    year: int
        Year of the election results.
    save_folder: int
        Location of the folder where the year's election results are stored.

    Returns
    -------
    election_dataframe: DataFrame
        Election results with the MIR's format.

    """

    if file_name:

        try:

            election_dataframe = _file_to_df(file_name)

        except:

            print("File Not Found!")
    else:

        file_name = save_folder + "/" + _get_file_name(year)

        try:

            election_dataframe = _file_to_df(file_name)

        except:

            _download_election(year=year, save_folder=save_folder)

            election_dataframe = _file_to_df(file_name)

    return election_dataframe


def clean_mir(df):
    """Extract the parties, regions, votes and distribution of mps from MIR's format.

    From the MIR's dataframe format, the function obtains the political parties, voting
    regions, votes per region and party, and distribution of mps following the input
    format used by electopy.

    Parameters
    ----------
    df: DataFrame
        Election results with the MIR's format.

    Returns
    -------
    parties: Series
        Political parties in the election.
    regions: Series
        Voting regions in the election.
    votes: DataFrame
        Votes per region per party in the election result.
    distribution: Series
        Allocated distribution of electable mps per voting region.

    """

    parties = _get_parties(df)
    regions = _get_voting_regions(df)
    votes = _get_votes(df)
    mps = _get_mps(df)
    distribution = _distribution_of_mps(mps)

    return parties, regions, votes, distribution


def clean_df(votes, distribution):
    """Extract the parties, regions and votes from a custom dataframe format.

    From a custom dataframe, the function obtains the political parties, voting regions
     and votes per region and party following the input format used by electopy.

    The dataframe format assumes that the columns have the parties' names and the row
    index has the voting regions names. All the values in the dataframe represent the
    votes received per political party in each voting region.

    The distribution of mps has to be provided separately as a series with the index of
    the series being the name of the voting region, and the value of each series the
    number of elected mps allocated to that voting region.

    Parameters
    ----------
    votes: DataFrame
        Votes per region per party from the election result.
    distribution: Series
        Allocated distribution of electable mps per voting region.

    Returns
    -------
    parties: Series
        Political parties in the election.
    regions: Series
        Voting regions in the election.
    votes: DataFrame
        Votes per region per party in the election result.
    distribution: Series
        Allocated distribution of electable mps per voting region.

    """

    regions = pd.Series(data=range(len(votes.index)), index=votes.index)
    votes.rename(regions, inplace=True)
    distribution.rename(regions, inplace=True)
    regions = pd.Series(data=regions.index.str.strip(), index=regions)

    parties = pd.Series(data=range(len(votes.columns)), index=votes.columns)
    votes.rename(columns=parties, inplace=True)
    parties = pd.Series(data=parties.index.str.strip(), index=parties)

    return parties, regions, votes, distribution


def _get_mir_dictionary():
    """Return a dictionary with the file name for each election year.

    A dictionary that contains the file name of the zip file for each election year
    in the MIR's web page.

    Returns
    -------
    election_mir_dictionary: dict
        Dictionary with the file name for each year's extension.
    
    """

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


def _get_file_name(year=2016):
    """Obtain the name of the file for the election results of a year.

    Get the name of the file for the election of the given year. If the year provided
    is not in the dictionary of files in the MIR, return the year 2016 file name.

    Parameters
    ----------
    year: int
        Year of the election.
    
    Returns
    -------
    file_name: str
        File name.
    
    """

    mir_dictionary = _get_mir_dictionary()

    try:

        file_name = mir_dictionary[year]

    except:

        print("Can not find the year of the election. 2016 will be loaded")

        file_name = mir_dictionary[2016]

    return file_name


def _download_election(year=2016, save_folder="past_elections"):
    """Download for the Ministry's of Interior web page the election results.

    Download from the MIR's web page the zip file for the election in "year", and
    saves it in the "save_folder".

    Parameters
    ----------
    year: int
        Year of the election.
    save_folder: str
        Location of folder where election file is saved.

    """

    MIR_ADDRESS = "http://www.infoelectoral.mir.es/infoelectoral/docxl/"
    file_name = _get_file_name(year)

    url = MIR_ADDRESS + file_name
    save_location = save_folder + "/" + file_name

    urllib.request.urlretrieve(url, save_location)


def _file_to_df(file_name):
    """Transform election file into a dataframe.

    Get the saved file with the election. If it is in a zip file, unzip it and obtain
    the excel file. Read the excel file into a  dataframe.

    Parameters
    ----------
    file_name: str
        Name of the name of the election file.

    Returns
    -------
    election_dataframe: DataFrame
        Election results with the MIR's format.

    """

    if file_name.endswith(".zip"):

        excel_file_name = file_name.rsplit("/")[-1][:-4] + ".xlsx"
        archive = zipfile.ZipFile(file_name, "r")
        excel_file = archive.open(excel_file_name)

    else:

        excel_file = file_name

    # nrows=54 works because the number of regions is the same for all elections. If there were any changes it wouldn't work

    election_dataframe = pd.read_excel(excel_file, skiprows=range(3), nrows=54)

    return election_dataframe


def _get_parties(df):
    """"Obtain the name of the political parties in the election.

    From the format of the MIR, get the name of all the political parties present in the
    election. Codify those political parties, and save the names with their code as a
    series. Political parties are the columns.

    Parameters
    ----------
    df: DataFrame
        Election results with the MIR's format.

    Returns
    -------
    parties: Series
        Political parties in the election.

    """

    parties = df.loc[0, (df.loc[1] == "Votos")].str.strip()

    parties.index = range(len(parties))
    parties.name = "Parties"

    return parties


def _get_voting_regions(df):
    """"Obtain the name of the voting regions in the election.

    From the format of the MIR, get the name of all the voting regions present in the
    election. Codify those voting regions, and save the names with their code as a
    series. Voting regions are the rows.

    Parameters
    ----------
    df: DataFrame
        Election results with the MIR's format.

    Returns
    -------
    regions: Series
        Voting regions in the election.

    """

    col_name = df.columns[df.loc[1] == "Nombre de Provincia"]
    col_code = df.columns[df.loc[1] == "Código de Provincia"]

    regions = df.loc[2:, col_name].iloc[:, 0].str.strip()
    regions.index = df.loc[2:, col_code].iloc[:, 0]

    regions.index.name = None
    regions.name = "Provincias"

    return regions


def _get_votes(df):
    """Create the dataframe with the votes for the election.

    Properly format the dataframe for the votes in the election. The columns of the
    dataframe are the political parties, and the rows are the voting regions. All the
    votes are given by political party per region. Columns and rows are indexed with the
    codification of regions and parties, instead of their name.

    Parameters
    ----------
    df: DataFrame
        Election results with the MIR's format.

    Returns
    -------
    votes: DataFrame
        Votes per region per party in the election result.

    """

    parties = _get_parties(df)
    col_code = df.columns[df.loc[1] == "Código de Provincia"]

    votes = df.loc[2:, (df.loc[1] == "Votos")]
    votes.columns = parties.index

    votes = votes.set_index(df.loc[2:, col_code].values.squeeze())

    return votes


def _get_mps(df):
    """Create a dataframe with the elected members of parliament (mps) for the election.

    Create a formated dataframe with the elected mps in the election. The columns of the
    dataframe are the political parties, and the rows are the voting regions. All the
    mps are given by political party per region. Columns and rows are indexed with the
    codification of regions and parties, instead of their name.

    Parameters
    ----------
    df: DataFrame
        Election results with the MIR's format.

    Returns
    -------
    mps: DataFrame
        Mps per region per party in the election result.

    """

    parties = _get_parties(df)
    col_code = df.columns[df.loc[1] == "Código de Provincia"]

    mps = df.loc[2:, (df.loc[1] == "Diputados")]
    mps.columns = parties.index

    mps = mps.set_index(df.loc[2:, col_code].values.squeeze())

    return mps


def _distribution_of_mps(mps):
    """Get the elected members of parliament (mps) for each region.

    Using the elected mps dataframe with the resulting mps elected per party per region,
    we obtain the distribution of mps per voting region in play in the elections. The
    elected mps per region are given as a series.

    Parameters
    ----------
    mps: DataFrame
        Mps per region per party in the election result.

    Returns
    -------
    distribution: Series
        Allocated distribution of electable mps per voting region.

    """

    distribution = mps.sum(axis=1).astype(int)

    return distribution


# cSpell: ignore inplace astype iloc rsplit nrows xlsx Diputados Código Votos Nombre
# cSpell: ignore MIR's PROV Provincia Provincias