"""_529.py

SpiralBevelRateableGear
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_RATEABLE_GEAR = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'SpiralBevelRateableGear')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelRateableGear',)


class SpiralBevelRateableGear(_0.APIBase):
    """SpiralBevelRateableGear

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_RATEABLE_GEAR

    def __init__(self, instance_to_wrap: 'SpiralBevelRateableGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_blank_temperature(self) -> 'float':
        """float: 'GearBlankTemperature' is the original name of this property."""

        temp = self.wrapped.GearBlankTemperature

        if temp is None:
            return None

        return temp

    @gear_blank_temperature.setter
    def gear_blank_temperature(self, value: 'float'):
        self.wrapped.GearBlankTemperature = float(value) if value else 0.0
