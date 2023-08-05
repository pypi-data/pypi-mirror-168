"""
This class is adapted from: https://github.com/jazzband/geojson/blob/master/geojson/feature.py
"""

from tfcat.base import Base
from tfcat.crs import DefaultCRS, CRS
from tfcat.validate import JSONSCHEMA_URI
from astropy.table import Table, Column
from tfcat.utils import split_coords
from astropy.time import Time
from shapely.geometry import shape
from matplotlib import pyplot as plt


class Feature(Base):
    """
    Represents a TF feature
    """ 

    def __init__(self, id=None,
                 geometry=None, properties=None, **extra):
        """
        Initialises a Feature object with the given parameters.

        :param id: Feature identifier, such as a sequential number.
        :type id: str, int
        :param geometry: Geometry corresponding to the feature.
        :param properties: Dict containing properties of the feature.
        :type properties: dict
        :return: Feature object
        :rtype: Feature
        """
        super(Feature, self).__init__(**extra)
        self["id"] = id
        self["geometry"] = (self.to_instance(geometry, strict=True)
                            if geometry else None)
        self["properties"] = properties or {}

    def errors(self):
        geo = self.get('geometry')
        return geo.errors() if geo else None

    @property
    def tmin(self):
        return self.bbox[0]
        #return self.geometry.tmin #numpy.min([item[0] for item in self.geometry.coordinates]) if self.geometry else None

    @property
    def tmax(self):
        return self.bbox[2]
        #return self.geometry.tmax # numpy.max([item[0] for item in self.geometry.coordinates]) if self.geometry else None

    @property
    def fmin(self):
        return self.bbox[1]
        #return self.geometry.fmin # numpy.min([item[1] for item in self.geometry.coordinates]) if self.geometry else None

    @property
    def fmax(self):
        return self.bbox[3]
        #return self.geometry.fmax # numpy.max([item[1] for item in self.geometry.coordinates]) if self.geometry else None

    @property
    def bbox(self):
        #return [self.tmin, self.fmin, self.tmax, self.fmax] if self.geometry else None
        return shape(self.geometry).bounds if self.geometry else None

    def __len__(self):
        return len(self.geometry.coordinates) if self.geometry else 0

    def _plot(self, crs=None):

        ftype = self['geometry']['type']
        coord = self['geometry']['coordinates']
        if ftype not in ['MultiLineString', 'MultiPolygon']:
            coord = [coord]

        plot_style = '+-'
        if ftype.endswith('Point'):
            plot_style = '+'

        for item in coord:
            itimes, ifreqs = split_coords(item, crs=crs)
            if crs is not None:
                plt.plot(itimes.datetime, ifreqs.value, plot_style)
            else:
                plt.plot(itimes, ifreqs, plot_style)

    def _plot_bbox(self, crs=None):
        bbox_times = [self.tmin, self.tmax, self.tmax, self.tmin, self.tmin]
        if crs is not None:
            bbox_times = crs.time_converter(bbox_times).datetime
        bbox_freqs = [self.fmin, self.fmin, self.fmax, self.fmax, self.fmin]
        plt.plot(bbox_times, bbox_freqs, '--', label='bbox')

    def plot(self, crs=None):

        self._plot(crs)
        self._plot_bbox(crs)

        if crs is not None:
            plt.xlabel(crs.properties['time_coords']['name'])
            plt.ylabel(f"{crs.properties['spectral_coords']['name']} ({crs.properties['spectral_coords']['unit']})")

        plt.title(f"({self['geometry']['type']})")

        plt.show()


class FeatureCollection(Base):
    """
    Represents a FeatureCollection, a set of multiple Feature objects.
    """

    def __init__(self, features=None, properties=None, fields=None, crs=None, schema=JSONSCHEMA_URI, **extra):
        """
        Initialises a FeatureCollection object from the

        :param features: List of features to constitute the FeatureCollection.
        :type features: list
        :return: FeatureCollection object
        :rtype: FeatureCollection
        """
        super(FeatureCollection, self).__init__(**extra)
        self["$schema"] = schema
        self["features"] = features
        self["fields"] = fields or {}
        self["properties"] = properties or {}
        self["crs"] = CRS(crs=crs) or DefaultCRS

    def errors(self):
        return self.check_list_errors(lambda x: x.errors(), self.features)

    def __getitem__(self, key):
        try:
            return self.get("features", ())[key]
        except (KeyError, TypeError, IndexError):
            return super(Base, self).__getitem__(key)

    def __len__(self):
        return len(self.features)

    def as_table(self):
        """
        produces a Astropy Table object containing the TFCat data

        :return:
        :rtype: Table
        """

        cols = [
            FeatureColumn(
                name='feature',
                data=[item.geometry for item in self.features],
                description='Feature',
                crs=self.crs
            ),
            Column(
                name='tmin',
                data=[self.crs.time_converter(item.bbox[0]).datetime for item in self.features],
                description='Feature Start Time'
            ),
            Column(
                name='tmax',
                data=[self.crs.time_converter(item.bbox[2]).datetime for item in self.features],
                description='Feature End Time'
            ),
            Column(
                name='fmin',
                data=[item.bbox[1] for item in self.features],
                unit=self.crs.properties['spectral_coords']['unit'],
                description='Feature lower spectral bound'
            ),
            Column(
                name='fmax',
                data=[item.bbox[3] for item in self.features],
                unit=self.crs.properties['spectral_coords']['unit'],
                description='Feature upper spectral bound'
            )
        ]

        for key in self.fields:
            cur_col = Column(
                name=key,
                dtype=self.fields[key]['datatype'],
                data=[item.properties[key] for item in self.features],
                unit=self.fields[key].get('unit', None),
                description=self.fields[key].get('info', None)
            )
            if 'values' in self.fields[key]:
                cur_col.meta = {'options': self.fields[key].get('values', None)}
            cols.append(cur_col)

        return Table(cols)


class FeatureColumn(Column):

    def __new__(cls, crs=None, **extra):
        self = super().__new__(cls, **extra)
        self._crs = crs or DefaultCRS
        return self

    @property
    def type(self):
        return Column([item['type'] for item in self])

    def coordinates(self, ifeature): #, time_format=None, spectral_unit=None):
        return split_coords(self[ifeature], self._crs)



