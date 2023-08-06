"""_788.py

BasicConicalGearMachineSettingsFormate
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _787
from mastapy._internal.python_net import python_net_import

_BASIC_CONICAL_GEAR_MACHINE_SETTINGS_FORMATE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings', 'BasicConicalGearMachineSettingsFormate')


__docformat__ = 'restructuredtext en'
__all__ = ('BasicConicalGearMachineSettingsFormate',)


class BasicConicalGearMachineSettingsFormate(_787.BasicConicalGearMachineSettings):
    """BasicConicalGearMachineSettingsFormate

    This is a mastapy class.
    """

    TYPE = _BASIC_CONICAL_GEAR_MACHINE_SETTINGS_FORMATE

    def __init__(self, instance_to_wrap: 'BasicConicalGearMachineSettingsFormate.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def horizontal_setting(self) -> 'float':
        """float: 'HorizontalSetting' is the original name of this property."""

        temp = self.wrapped.HorizontalSetting

        if temp is None:
            return None

        return temp

    @horizontal_setting.setter
    def horizontal_setting(self, value: 'float'):
        self.wrapped.HorizontalSetting = float(value) if value else 0.0

    @property
    def vertical_setting(self) -> 'float':
        """float: 'VerticalSetting' is the original name of this property."""

        temp = self.wrapped.VerticalSetting

        if temp is None:
            return None

        return temp

    @vertical_setting.setter
    def vertical_setting(self, value: 'float'):
        self.wrapped.VerticalSetting = float(value) if value else 0.0
