"""electopy.display

This module contains all the necessary functions to create graphical representations of
the elections for the electopy.election object.

"""

import electopy.display

import numpy as np

import urllib.request
import zipfile

import geopandas as gpd
import shapely

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import to_hex


def get_spain_map(x=0.0, y=0.0):
    """Obtain the geographic data representing the map of Spain.

    Create a GeoPandas dataframe with the geographic data for each voting region in
    Spain. Needed to create a map representation of the election results.

    The shape file is obtained from Natural Earth Data. If it is not found it downloads
    the Admin1 global map, and then chooses only the regions for Spain.

    Parameters
    ----------
    x: float
        X-coordinate move of the Canary Islands from original position.
    y: float
        Y-coordinate move of the Canary Islands from original position.

    Returns
    -------
    esp: GeoPandas.DataFrame
        Geographic information (including geographic shape) for each region in Spain.

    """

    FILE_NAME = "ne_10m_admin_1_states_provinces.zip"
    SHAPE_LOCATION = "map/ne_10m_admin_1_states_provinces.shp"

    try:

        map_df = gpd.read_file(SHAPE_LOCATION)

    except:

        try:

            _unzip_file(FILE_NAME)

        except:

            _download_map()

        map_df = gpd.read_file(SHAPE_LOCATION)

    spa = map_df.loc[map_df["iso_a2"] == "ES"].copy()

    esp = electopy.display._move_canary(spa, x=x, y=y)

    return esp


def proper_names(esp):
    """Change the region names in Natural Earth Data to correctly spelt names.

    Adapt the names of the regions from the Natural Earth Data Admin1 dataset, to the
    names used by the Ministry of Interior for reporting its electoral results.

    Parameters
    ----------
    esp: GeoPandas.DataFrame
        Geographic information for each region in Spain.

    Returns
    -------
    esp: GeoPandas.DataFrame
        New geographic information for each region in Spain with correct names.

    """

    mapdict = electopy.display._correct_region_names()

    esp = esp.assign(prov=esp["name"].replace(mapdict))

    esp = esp.set_index("prov")

    return esp


def create_map_plot(merge, colormap, text, show=True):
    """Display map of Spain with most voted party per region.

    Create and display the plot with the map of Spain, showing which party earned the
    most votes in each voting region.

    Parameters
    ----------
    merge: GeoPandas.DataFrame
        The shapes of the regions and the most voted party for each region.
    colormap: list
        The display colors used to create the map.
    text: str
        Additional text to add to the plot title.
    show: bool
        Indicate if the plot should be displayed.

    Returns
    -------
    ax: plot
        Map of Spain with the most voted party in each region.

    """

    ax = merge.plot(
        column=0,
        cmap=colormap,
        linewidth=0.8,
        edgecolor="0.8",
        legend=True,
        categorical=True,
        legend_kwds={"loc": "lower right"},
    )
    ax.set_axis_off()
    ax.set_title("Winner by region: " + text)

    if show:

        plt.show()

    return ax


def create_parliament_labels(parl, limit=6):
    """Format the party labels shown in the parliament composition.

    Create the labels used to display the party names in the parliament composition.
    Limit is used to only show the most voted political parties. Parties over the limit
    will have an empty label.

    Parameters
    ----------
    parl: Series
        Ordered list of all political parties with representation in parliament.
    limit: int
        Maximum number of parties which have a label on the plot.

    Returns
    -------
    label: list
        The labels used to plot the parties' names in parliament composition.

    """

    label = list(parl.index)

    for i, v in enumerate(label):

        if parl[v] < limit:

            label[i] = ""

    return label


def create_parliament_plot(sortedparl, colors, label, text, show=True):
    """Display plot showing the parliament composition.

    Create and display a pie chart, showing the total number of elected mps in the
    parliament for each political party.

    Parameters
    ----------
    sortedparl: Series
        Number of elected mps for each party, sorted by number of mps.
    colors: list
        The display colors used to create the plot.
    label: list
        Names of political parties to display in the plot.
    text: str
        Additional text to add to the plot title.
    show: bool
        Indicate if the plot should be displayed.

    Returns
    -------
    ax: plot
        Parliament composition by political party.

    """

    ax = plt.pie(
        sortedparl,
        colors=colors,
        wedgeprops=dict(width=0.5),
        startangle=90,
        labels=label,
        autopct=lambda x: electopy.display._display(x),
        pctdistance=0.75,
        textprops={"fontsize": "large", "weight": "bold"},
    )
    plt.title("parliament composition: " + text, fontdict={"fontsize": 32})

    if show:

        plt.show()

    return ax


def create_colors(parties):
    """Make a list of colors for plots.

    Create the list of colors used to display. If the party exists in the party_colors
    dictionary, use the party's corresponding colour. Else use a random colour.

    Parameters
    ----------
    parties: list
        Names of parties which are displayed in the plot.

    Returns
    -------
    cmap: list
        List of colors used in the plot.

    """

    partycolors = _party_colors()

    colormap = np.vectorize(partycolors.get)(parties)

    missing = np.sum(colormap == "None")

    if missing > 10:

        extracolors = cm.get_cmap("tab20", 20)(np.linspace(0, 1, 20))

    else:

        extracolors = cm.get_cmap("tab10", 10)(np.linspace(0, 1, 10))

    i = 0
    cmap = []

    for party in parties:

        try:

            c = partycolors[party]

        except:

            c = extracolors[i]
            i += 1

        cmap.append(c)

    return cmap


def _download_map():
    """Dowload Natural Earth Data map information.

    Downloads for the Natural Earth Data the Admin 1 map, which contains the
    geographical shapes of each region in the world. Importantly, for Spain, these match
    the voting regions. The shapes are used to create plots with the map of Spain.

    """

    SAVE_FOLDER = "map"
    MAP_ADDRESS = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/"
    FILE_NAME = "ne_10m_admin_1_states_provinces.zip"

    url = MAP_ADDRESS + FILE_NAME
    save_location = SAVE_FOLDER + "/" + FILE_NAME

    urllib.request.urlretrieve(url, save_location)

    unzip_file(FILE_NAME)


def _unzip_file(file_name):
    """Unzip files from Natural Earth Data map.

    Once downloaded the zip file from NED, unzip the file in the save folder.

    Parameters
    ----------
    file_name: str
        Name of file to unzip.

    """

    SAVE_FOLDER = "map"

    save_location = SAVE_FOLDER + "/" + file_name

    zip_ref = zipfile.ZipFile(save_location, "r")
    zip_ref.extractall(SAVE_FOLDER + "/")
    zip_ref.close()


def _move_canary(geo, x=0, y=0):
    """Change the geographic position of the Canary Islands (CI).

    Get a GeoPandas dataframe with geographical data for all regions in spain, and
    transform the x and y coordinates of the geographic data of the regions which are
    part of the Canary Islands (adm0_sr == 3).

    Parameters
    ----------
    geo: GeoPandas.DataFrame
        Geographic information (including geographic shape) for each region in Spain.
    x: float
        X-coordinate move of the Canary Islands from original position.
    y: float
        Y-coordinate move of the Canary Islands from original position.

    Returns
    -------
    geo: GeoPandas.DataFrame
        New geographic information for each region in Spain, including changes in CI.

    """

    geo.loc[geo["adm0_sr"] == 3, "geometry"] = geo.loc[
        geo["adm0_sr"] == 3, "geometry"
    ].apply(lambda n: shapely.affinity.translate(n, xoff=x, yoff=y))

    return geo


## cSpell: disable


def _correct_region_names():
    """Dictionary with correct spelling of region names.

    Natural Earth Data (NED) has the names of the regions with different spelling than 
    those used by the Ministry of Interior (MIR) in Spain for electoral data. This
    function returns a dictionary for every mispelt region in NED with the corresponding
    correct spelling used in MIR.

    Returns
    -------
    mapdict: dict
        Mapping of mispelt regions to their correct spelling.

    """

    mapdict = {
        "CÃ¡ceres": "Cáceres",
        "Orense": "Ourense",
        "CÃ¡diz": "Cádiz",
        "CastellÃ³n": "Castellón / Castelló",
        "Castellón": "Castellón / Castelló",
        "AlmerÃ­a": "Almería",
        "MÃ¡laga": "Málaga",
        "La CoruÃ±a": "A Coruña",
        "La Coruña": "A Coruña",
        "Ãlava": "Araba - Álava",
        "Álava": "Araba - Álava",
        "LeÃ³n": "León",
        "Ãvila": "Ávila",
        "CÃ³rdoba": "Córdoba",
        "JaÃ©n": "Jaén",
        "Alicante": "Alicante / Alacant",
        "Valencia": "Valencia / València",
        "Baleares": "Illes Balears",
        "Gerona": "Girona",
        "LÃ©rida": "Lleida",
        "Lérida": "Lleida",
    }

    return mapdict


def _party_colors():
    """Dictionary with political parties and their corresponding color.

    Return a dictionary with some political parties and the color normally used to
    represent the party visually.

    Returns
    -------
    pc: dict
        Dictionary with partie's name and their color.

    """

    pc = {
        "PSOE": "#ED1C24",
        "PP": "#0055A7",
        "Cs": "#FA5000",
        "C's": "#FA5000",
        "Podemos": "#6A2E68",
        "PODEMOS-IU-EQUO": "#6A2E68",
        "ECP": "#6A2E68",
        "PODEMOS-EN MAREA-ANOVA-EU": "#6A2E68",
        "VOX": "#5AC035",
        "ERC": "#F3B217",
        "ERC-CATSÍ": "#F3B217",
        "CDC": "#C40048",
        "JxCAT": "#C40048",
        "PNV": "#009526",
        "EAJ-PNV": "#009526",
        "EH Bildu": "#A3C940",
        "NA+": "#FFDA1A",
        "CC": "#E51C13",
        "CCa-PNC": "#E51C13",
        "PRC": "#DB6426",
        "COMPROMÍS": "#BECD48",
        "PODEMOS-COMPROMÍS-EUPV": "#BECD48",
    }

    return pc


## cSpell: enable


def _display(pct):
    """Function used to display the number of mps obtained by each party.

    The function returns a string to display, if the party has obtained more than 1.5%
    of the total mps. The percentage is multiplied by 3.5 in order to represent the
    number of mps instead of the percentage. Currently there are 350 mps in the Spanish
    parliament.

    Parameter
    ---------
    pct: float
        Percentage value.

    Returns
    -------
    :str
        Number of mps.

    """

    if pct > 1.5:

        return "{:.0f}".format(pct * 3.5)


## cSpell: ignore xoff yoff cmap vectorize prov parl sortedparl colormap edgecolor autopct pctdistance fontdict
