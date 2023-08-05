from tfcat.base import Base
from astropy.units import Unit, Quantity


class Field(Base):

    def __init__(self, info=None, datatype=None, ucd=None, unit=None, **extra):
        super(Field).__init__(**extra)
        self.info = info
        self.datatype = datatype
        self.ucd = ucd
        self.unit = unit
