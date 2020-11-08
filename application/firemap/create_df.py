import pandas as pd
import numpy as np


def create_modis_arc_df(date):
    yy, mm, dd = date.split("-")
    acq_date = mm.lstrip('0') + '/' + dd.lstrip('0') + '/' + yy
    mapData = pd.read_csv('application/firemap/Data/West_Africa_MODIS_FireHotspots.csv')
    mapData['acq_date'] = pd.to_datetime(mapData['acq_date'])
    modis_fires = mapData[mapData['acq_date'] == acq_date]

    if len(modis_fires) != 0:
        modis_fires = pd.DataFrame(data=modis_fires)
    else:
        modis_fires = pd.DataFrame(np.nan, index=[0], columns=['latitude', 'longitude'])
    return modis_fires


def create_modis_all_df():
    all_Data = pd.read_csv('application/firemap/Data/West_Africa_MODIS_FireHotspots.csv')

    return all_Data


def create_viirs_arc_df(date):
    yy, mm, dd = date.split("-")
    acq_date = mm.lstrip('0') + '/' + dd.lstrip('0') + '/' + yy
    mapData = pd.read_csv('application/firemap/Data/West_Africa_VIIRS_FireHotspots.csv')
    mapData['acq_date'] = pd.to_datetime(mapData['acq_date'])
    viirs_fires = mapData[mapData['acq_date'] == acq_date]

    if len(viirs_fires) != 0:
        viirs_fires = pd.DataFrame(data=viirs_fires)

    else:
        viirs_fires = pd.DataFrame(np.nan, index=[0], columns=['latitude', 'longitude'])
    return viirs_fires


def create_viirs_all_df():
    all_Data = pd.read_csv('application/firemap/Data/West_Africa_VIIRS_FireHotspots.csv')

    return all_Data


def create_graph_df():
    graphData = pd.read_csv('application/firemap/Data/West_Africa_Monthly_FireCounts.csv')
    graph_df = graphData
    return graph_df
