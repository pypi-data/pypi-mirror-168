"""_789.py

BasicConicalGearMachineSettingsGenerated
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _787
from mastapy._internal.python_net import python_net_import

_BASIC_CONICAL_GEAR_MACHINE_SETTINGS_GENERATED = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings', 'BasicConicalGearMachineSettingsGenerated')


__docformat__ = 'restructuredtext en'
__all__ = ('BasicConicalGearMachineSettingsGenerated',)


class BasicConicalGearMachineSettingsGenerated(_787.BasicConicalGearMachineSettings):
    """BasicConicalGearMachineSettingsGenerated

    This is a mastapy class.
    """

    TYPE = _BASIC_CONICAL_GEAR_MACHINE_SETTINGS_GENERATED

    def __init__(self, instance_to_wrap: 'BasicConicalGearMachineSettingsGenerated.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def basic_cradle_angle(self) -> 'float':
        """float: 'BasicCradleAngle' is the original name of this property."""

        temp = self.wrapped.BasicCradleAngle

        if temp is None:
            return None

        return temp

    @basic_cradle_angle.setter
    def basic_cradle_angle(self, value: 'float'):
        self.wrapped.BasicCradleAngle = float(value) if value else 0.0

    @property
    def blank_offset(self) -> 'float':
        """float: 'BlankOffset' is the original name of this property."""

        temp = self.wrapped.BlankOffset

        if temp is None:
            return None

        return temp

    @blank_offset.setter
    def blank_offset(self, value: 'float'):
        self.wrapped.BlankOffset = float(value) if value else 0.0

    @property
    def modified_roll_coefficient_c(self) -> 'float':
        """float: 'ModifiedRollCoefficientC' is the original name of this property."""

        temp = self.wrapped.ModifiedRollCoefficientC

        if temp is None:
            return None

        return temp

    @modified_roll_coefficient_c.setter
    def modified_roll_coefficient_c(self, value: 'float'):
        self.wrapped.ModifiedRollCoefficientC = float(value) if value else 0.0

    @property
    def modified_roll_coefficient_d(self) -> 'float':
        """float: 'ModifiedRollCoefficientD' is the original name of this property."""

        temp = self.wrapped.ModifiedRollCoefficientD

        if temp is None:
            return None

        return temp

    @modified_roll_coefficient_d.setter
    def modified_roll_coefficient_d(self, value: 'float'):
        self.wrapped.ModifiedRollCoefficientD = float(value) if value else 0.0

    @property
    def radial_setting(self) -> 'float':
        """float: 'RadialSetting' is the original name of this property."""

        temp = self.wrapped.RadialSetting

        if temp is None:
            return None

        return temp

    @radial_setting.setter
    def radial_setting(self, value: 'float'):
        self.wrapped.RadialSetting = float(value) if value else 0.0

    @property
    def ratio_of_roll(self) -> 'float':
        """float: 'RatioOfRoll' is the original name of this property."""

        temp = self.wrapped.RatioOfRoll

        if temp is None:
            return None

        return temp

    @ratio_of_roll.setter
    def ratio_of_roll(self, value: 'float'):
        self.wrapped.RatioOfRoll = float(value) if value else 0.0
