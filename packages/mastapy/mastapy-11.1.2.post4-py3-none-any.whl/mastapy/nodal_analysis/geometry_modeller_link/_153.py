"""_153.py

GeometryModellerLengthDimension
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.geometry_modeller_link import _147
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_LENGTH_DIMENSION = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerLengthDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerLengthDimension',)


class GeometryModellerLengthDimension(_147.BaseGeometryModellerDimension):
    """GeometryModellerLengthDimension

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_LENGTH_DIMENSION

    def __init__(self, instance_to_wrap: 'GeometryModellerLengthDimension.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return None

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0
