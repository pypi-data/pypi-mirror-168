"""_2358.py

TorqueConverterSpeedRatio
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_SPEED_RATIO = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterSpeedRatio')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterSpeedRatio',)


class TorqueConverterSpeedRatio(_0.APIBase):
    """TorqueConverterSpeedRatio

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_SPEED_RATIO

    def __init__(self, instance_to_wrap: 'TorqueConverterSpeedRatio.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def inverse_k(self) -> 'float':
        """float: 'InverseK' is the original name of this property."""

        temp = self.wrapped.InverseK

        if temp is None:
            return None

        return temp

    @inverse_k.setter
    def inverse_k(self, value: 'float'):
        self.wrapped.InverseK = float(value) if value else 0.0

    @property
    def speed_ratio(self) -> 'float':
        """float: 'SpeedRatio' is the original name of this property."""

        temp = self.wrapped.SpeedRatio

        if temp is None:
            return None

        return temp

    @speed_ratio.setter
    def speed_ratio(self, value: 'float'):
        self.wrapped.SpeedRatio = float(value) if value else 0.0

    @property
    def torque_ratio(self) -> 'float':
        """float: 'TorqueRatio' is the original name of this property."""

        temp = self.wrapped.TorqueRatio

        if temp is None:
            return None

        return temp

    @torque_ratio.setter
    def torque_ratio(self, value: 'float'):
        self.wrapped.TorqueRatio = float(value) if value else 0.0
