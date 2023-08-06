"""_642.py

HobManufactureError
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _655
from mastapy._internal.python_net import python_net_import

_HOB_MANUFACTURE_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobManufactureError')


__docformat__ = 'restructuredtext en'
__all__ = ('HobManufactureError',)


class HobManufactureError(_655.RackManufactureError):
    """HobManufactureError

    This is a mastapy class.
    """

    TYPE = _HOB_MANUFACTURE_ERROR

    def __init__(self, instance_to_wrap: 'HobManufactureError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_relief_variation(self) -> 'float':
        """float: 'TotalReliefVariation' is the original name of this property."""

        temp = self.wrapped.TotalReliefVariation

        if temp is None:
            return None

        return temp

    @total_relief_variation.setter
    def total_relief_variation(self, value: 'float'):
        self.wrapped.TotalReliefVariation = float(value) if value else 0.0

    @property
    def use_sin_curve_for_top_relief(self) -> 'bool':
        """bool: 'UseSinCurveForTopRelief' is the original name of this property."""

        temp = self.wrapped.UseSinCurveForTopRelief

        if temp is None:
            return None

        return temp

    @use_sin_curve_for_top_relief.setter
    def use_sin_curve_for_top_relief(self, value: 'bool'):
        self.wrapped.UseSinCurveForTopRelief = bool(value) if value else False
