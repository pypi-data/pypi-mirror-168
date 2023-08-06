"""_148.py

GeometryModellerAngleDimension
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.geometry_modeller_link import _147
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_ANGLE_DIMENSION = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerAngleDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerAngleDimension',)


class GeometryModellerAngleDimension(_147.BaseGeometryModellerDimension):
    """GeometryModellerAngleDimension

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_ANGLE_DIMENSION

    def __init__(self, instance_to_wrap: 'GeometryModellerAngleDimension.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle(self) -> 'float':
        """float: 'Angle' is the original name of this property."""

        temp = self.wrapped.Angle

        if temp is None:
            return None

        return temp

    @angle.setter
    def angle(self, value: 'float'):
        self.wrapped.Angle = float(value) if value else 0.0
