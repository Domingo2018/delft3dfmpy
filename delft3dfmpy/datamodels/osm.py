import os
import pickle

import geopandas as gpd
import pandas as pd

from delft3dfmpy.datamodels.common import ExtendedDataFrame, ExtendedGeoDataFrame
from shapely.geometry import LineString, Point, Polygon

class OSM:
    """
    OpenStreetMap model
    """

    def __init__(self, extent_file=None):

        # Read geometry to clip data
        if extent_file is not None:
            self.clipgeo = gpd.read_file(extent_file).unary_union
        else:
            self.clipgeo = None



        # Create standard dataframe for network, cross sections, orifices, weirs
        # FIXME: check available columns and required columns for the OSM data, and apply these here
        self.branches = ExtendedGeoDataFrame(geotype=LineString, required_columns=[
            'code',
            'geometry'
        ])

        # FIXME: in openstreetmap, cross sections are not linestrings, perpendicular to stream, but profile types and dimensions of a channel
        # It may be that this is "parameterised cross sections, and we simply don't need the property below.
        self.crosssections = ExtendedGeoDataFrame(geotype=LineString, required_columns=[
            'code',
            'geometry',
            'ruwheidswaarde',
            'ruwheidstypecode'
        ])

        # FIXME: ensure that all required parameterised properties are provided. I can imagine this is a matter of making
        # several parameterised profiles for different profile types (e.g. trapezoidal, rectangular, circular, etc.)
        self.parametrised_profiles = ExtendedGeoDataFrame(geotype=LineString, required_columns=[
            'code',
            'bodemhoogtebenedenstrooms',
            'bodemhoogtebovenstrooms',
            'bodembreedte',
            'taludhellinglinkerzijde',
            'taludhellingrechterzijde',
            'hoogteinsteeklinkerzijde',
            'hoogteinsteekrechterzijde',
            'ruwheidswaarde',
            'ruwheidstypecode'
        ])


        # FIXME: ensure that all culvert types and properties can be handled. We probably have circular and box-shaped culverts, sometimes with multiple openings
        self.culverts = ExtendedGeoDataFrame(geotype=LineString, required_columns=[
            'code',
            'geometry',
            'lengte',
            'hoogteopening',
            'breedteopening',
            'hoogtebinnenonderkantbenedenstrooms',
            'hoogtebinnenonderkantbovenstrooms',
            'vormcode',
            'intreeverlies',
            'uittreeverlies',
            'ruwheidstypecode',
            'ruwheidswaarde'
        ])
        # # FIXME: not sure what laterals in this context mean, but I don't think we need it at this stage.
        # self.laterals = ExtendedGeoDataFrame(geotype=Point, required_columns=[
        #     'code',
        #     'geometry'
        # ])
        #

    def to_pickle(self, filename, overwrite=False):
        # Check if path exists
        if os.path.exists(filename) and not overwrite:
            raise FileExistsError(f'File "{filename}" alraedy exists.')

        # Dump object
        with open(filename, 'wb') as handle:
            pickle.dump(self, handle)

    @classmethod
    def from_pickle(cls, filename):
        # Read object
        with open(filename, 'rb') as handle:
            loaded_cls = pickle.load(handle)

        return loaded_cls


