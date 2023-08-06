"""_149.py

GeometryModellerCountDimension
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.geometry_modeller_link import _147
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_COUNT_DIMENSION = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerCountDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerCountDimension',)


class GeometryModellerCountDimension(_147.BaseGeometryModellerDimension):
    """GeometryModellerCountDimension

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_COUNT_DIMENSION

    def __init__(self, instance_to_wrap: 'GeometryModellerCountDimension.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def count(self) -> 'int':
        """int: 'Count' is the original name of this property."""

        temp = self.wrapped.Count

        if temp is None:
            return None

        return temp

    @count.setter
    def count(self, value: 'int'):
        self.wrapped.Count = int(value) if value else 0
