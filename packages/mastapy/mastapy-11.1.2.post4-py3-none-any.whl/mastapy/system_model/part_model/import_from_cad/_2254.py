"""_2254.py

PlanetShaftFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2242
from mastapy._internal.python_net import python_net_import

_PLANET_SHAFT_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'PlanetShaftFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetShaftFromCAD',)


class PlanetShaftFromCAD(_2242.AbstractShaftFromCAD):
    """PlanetShaftFromCAD

    This is a mastapy class.
    """

    TYPE = _PLANET_SHAFT_FROM_CAD

    def __init__(self, instance_to_wrap: 'PlanetShaftFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planet_diameter(self) -> 'float':
        """float: 'PlanetDiameter' is the original name of this property."""

        temp = self.wrapped.PlanetDiameter

        if temp is None:
            return None

        return temp

    @planet_diameter.setter
    def planet_diameter(self, value: 'float'):
        self.wrapped.PlanetDiameter = float(value) if value else 0.0
