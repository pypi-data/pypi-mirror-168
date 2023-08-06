"""_155.py

GeometryModellerUnitlessDimension
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.geometry_modeller_link import _147
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_UNITLESS_DIMENSION = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerUnitlessDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerUnitlessDimension',)


class GeometryModellerUnitlessDimension(_147.BaseGeometryModellerDimension):
    """GeometryModellerUnitlessDimension

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_UNITLESS_DIMENSION

    def __init__(self, instance_to_wrap: 'GeometryModellerUnitlessDimension.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def value(self) -> 'float':
        """float: 'Value' is the original name of this property."""

        temp = self.wrapped.Value

        if temp is None:
            return None

        return temp

    @value.setter
    def value(self, value: 'float'):
        self.wrapped.Value = float(value) if value else 0.0
