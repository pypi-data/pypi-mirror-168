"""_779.py

PinionFinishCutter
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _1107
from mastapy._internal.python_net import python_net_import

_PINION_FINISH_CUTTER = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.Cutters', 'PinionFinishCutter')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionFinishCutter',)


class PinionFinishCutter(_1107.ConicalGearCutter):
    """PinionFinishCutter

    This is a mastapy class.
    """

    TYPE = _PINION_FINISH_CUTTER

    def __init__(self, instance_to_wrap: 'PinionFinishCutter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def inner_blade_point_radius_convex(self) -> 'float':
        """float: 'InnerBladePointRadiusConvex' is the original name of this property."""

        temp = self.wrapped.InnerBladePointRadiusConvex

        if temp is None:
            return None

        return temp

    @inner_blade_point_radius_convex.setter
    def inner_blade_point_radius_convex(self, value: 'float'):
        self.wrapped.InnerBladePointRadiusConvex = float(value) if value else 0.0

    @property
    def outer_blade_point_radius_concave(self) -> 'float':
        """float: 'OuterBladePointRadiusConcave' is the original name of this property."""

        temp = self.wrapped.OuterBladePointRadiusConcave

        if temp is None:
            return None

        return temp

    @outer_blade_point_radius_concave.setter
    def outer_blade_point_radius_concave(self, value: 'float'):
        self.wrapped.OuterBladePointRadiusConcave = float(value) if value else 0.0

    @property
    def radius(self) -> 'float':
        """float: 'Radius' is the original name of this property."""

        temp = self.wrapped.Radius

        if temp is None:
            return None

        return temp

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value else 0.0
