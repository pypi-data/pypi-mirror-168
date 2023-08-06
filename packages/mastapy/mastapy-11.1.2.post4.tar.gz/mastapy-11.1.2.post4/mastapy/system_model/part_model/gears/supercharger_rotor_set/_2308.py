"""_2308.py

RotorSetMeasuredPoint
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ROTOR_SET_MEASURED_POINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'RotorSetMeasuredPoint')


__docformat__ = 'restructuredtext en'
__all__ = ('RotorSetMeasuredPoint',)


class RotorSetMeasuredPoint(_0.APIBase):
    """RotorSetMeasuredPoint

    This is a mastapy class.
    """

    TYPE = _ROTOR_SET_MEASURED_POINT

    def __init__(self, instance_to_wrap: 'RotorSetMeasuredPoint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def boost_pressure(self) -> 'float':
        """float: 'BoostPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoostPressure

        if temp is None:
            return None

        return temp

    @property
    def input_power(self) -> 'float':
        """float: 'InputPower' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputPower

        if temp is None:
            return None

        return temp

    @property
    def rotor_speed(self) -> 'float':
        """float: 'RotorSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotorSpeed

        if temp is None:
            return None

        return temp
