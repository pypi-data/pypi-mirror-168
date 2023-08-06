"""_151.py

GeometryModellerDimensions
"""


from typing import List

from mastapy.nodal_analysis.geometry_modeller_link import (
    _148, _149, _153, _155
)
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_DIMENSIONS = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerDimensions')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerDimensions',)


class GeometryModellerDimensions(_0.APIBase):
    """GeometryModellerDimensions

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_DIMENSIONS

    def __init__(self, instance_to_wrap: 'GeometryModellerDimensions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_dimensions(self) -> 'List[_148.GeometryModellerAngleDimension]':
        """List[GeometryModellerAngleDimension]: 'AngleDimensions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngleDimensions

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def count_dimensions(self) -> 'List[_149.GeometryModellerCountDimension]':
        """List[GeometryModellerCountDimension]: 'CountDimensions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CountDimensions

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def length_dimensions(self) -> 'List[_153.GeometryModellerLengthDimension]':
        """List[GeometryModellerLengthDimension]: 'LengthDimensions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthDimensions

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def unitless_dimensions(self) -> 'List[_155.GeometryModellerUnitlessDimension]':
        """List[GeometryModellerUnitlessDimension]: 'UnitlessDimensions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UnitlessDimensions

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
