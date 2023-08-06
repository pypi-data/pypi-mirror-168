"""_2200.py

EnginePartLoad
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ENGINE_PART_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'EnginePartLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('EnginePartLoad',)


class EnginePartLoad(_0.APIBase):
    """EnginePartLoad

    This is a mastapy class.
    """

    TYPE = _ENGINE_PART_LOAD

    def __init__(self, instance_to_wrap: 'EnginePartLoad.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def consumption(self) -> 'float':
        """float: 'Consumption' is the original name of this property."""

        temp = self.wrapped.Consumption

        if temp is None:
            return None

        return temp

    @consumption.setter
    def consumption(self, value: 'float'):
        self.wrapped.Consumption = float(value) if value else 0.0

    @property
    def throttle(self) -> 'float':
        """float: 'Throttle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Throttle

        if temp is None:
            return None

        return temp

    @property
    def torque(self) -> 'float':
        """float: 'Torque' is the original name of this property."""

        temp = self.wrapped.Torque

        if temp is None:
            return None

        return temp

    @torque.setter
    def torque(self, value: 'float'):
        self.wrapped.Torque = float(value) if value else 0.0
