"""_782.py

WheelRoughCutter
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _1107
from mastapy._internal.python_net import python_net_import

_WHEEL_ROUGH_CUTTER = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.Cutters', 'WheelRoughCutter')


__docformat__ = 'restructuredtext en'
__all__ = ('WheelRoughCutter',)


class WheelRoughCutter(_1107.ConicalGearCutter):
    """WheelRoughCutter

    This is a mastapy class.
    """

    TYPE = _WHEEL_ROUGH_CUTTER

    def __init__(self, instance_to_wrap: 'WheelRoughCutter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delta_bg(self) -> 'float':
        """float: 'DeltaBG' is the original name of this property."""

        temp = self.wrapped.DeltaBG

        if temp is None:
            return None

        return temp

    @delta_bg.setter
    def delta_bg(self, value: 'float'):
        self.wrapped.DeltaBG = float(value) if value else 0.0

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
    def point_width(self) -> 'float':
        """float: 'PointWidth' is the original name of this property."""

        temp = self.wrapped.PointWidth

        if temp is None:
            return None

        return temp

    @point_width.setter
    def point_width(self, value: 'float'):
        self.wrapped.PointWidth = float(value) if value else 0.0

    @property
    def stock_allowance(self) -> 'float':
        """float: 'StockAllowance' is the original name of this property."""

        temp = self.wrapped.StockAllowance

        if temp is None:
            return None

        return temp

    @stock_allowance.setter
    def stock_allowance(self, value: 'float'):
        self.wrapped.StockAllowance = float(value) if value else 0.0
