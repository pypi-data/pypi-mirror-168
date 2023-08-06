"""_760.py

ConicalWheelManufacturingConfig
"""


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.bevel.basic_machine_settings import (
    _790, _787, _788, _789
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.cutters import _781, _782
from mastapy.gears.manufacturing.bevel import _742

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CONICAL_WHEEL_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalWheelManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalWheelManufacturingConfig',)


class ConicalWheelManufacturingConfig(_742.ConicalGearManufacturingConfig):
    """ConicalWheelManufacturingConfig

    This is a mastapy class.
    """

    TYPE = _CONICAL_WHEEL_MANUFACTURING_CONFIG

    def __init__(self, instance_to_wrap: 'ConicalWheelManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def use_cutter_tilt(self) -> 'bool':
        """bool: 'UseCutterTilt' is the original name of this property."""

        temp = self.wrapped.UseCutterTilt

        if temp is None:
            return None

        return temp

    @use_cutter_tilt.setter
    def use_cutter_tilt(self, value: 'bool'):
        self.wrapped.UseCutterTilt = bool(value) if value else False

    @property
    def wheel_finish_manufacturing_machine(self) -> 'str':
        """str: 'WheelFinishManufacturingMachine' is the original name of this property."""

        temp = self.wrapped.WheelFinishManufacturingMachine.SelectedItemName

        if temp is None:
            return None

        return temp

    @wheel_finish_manufacturing_machine.setter
    def wheel_finish_manufacturing_machine(self, value: 'str'):
        self.wrapped.WheelFinishManufacturingMachine.SetSelectedItem(str(value) if value else '')

    @property
    def wheel_rough_manufacturing_machine(self) -> 'str':
        """str: 'WheelRoughManufacturingMachine' is the original name of this property."""

        temp = self.wrapped.WheelRoughManufacturingMachine.SelectedItemName

        if temp is None:
            return None

        return temp

    @wheel_rough_manufacturing_machine.setter
    def wheel_rough_manufacturing_machine(self, value: 'str'):
        self.wrapped.WheelRoughManufacturingMachine.SetSelectedItem(str(value) if value else '')

    @property
    def specified_cradle_style_machine_settings(self) -> '_790.CradleStyleConicalMachineSettingsGenerated':
        """CradleStyleConicalMachineSettingsGenerated: 'SpecifiedCradleStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedCradleStyleMachineSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specified_machine_settings(self) -> '_787.BasicConicalGearMachineSettings':
        """BasicConicalGearMachineSettings: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedMachineSettings

        if temp is None:
            return None

        if _787.BasicConicalGearMachineSettings.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettings. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specified_machine_settings_of_type_basic_conical_gear_machine_settings_formate(self) -> '_788.BasicConicalGearMachineSettingsFormate':
        """BasicConicalGearMachineSettingsFormate: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedMachineSettings

        if temp is None:
            return None

        if _788.BasicConicalGearMachineSettingsFormate.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettingsFormate. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specified_machine_settings_of_type_basic_conical_gear_machine_settings_generated(self) -> '_789.BasicConicalGearMachineSettingsGenerated':
        """BasicConicalGearMachineSettingsGenerated: 'SpecifiedMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedMachineSettings

        if temp is None:
            return None

        if _789.BasicConicalGearMachineSettingsGenerated.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast specified_machine_settings to BasicConicalGearMachineSettingsGenerated. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def wheel_finish_cutter(self) -> '_781.WheelFinishCutter':
        """WheelFinishCutter: 'WheelFinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelFinishCutter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def wheel_rough_cutter(self) -> '_782.WheelRoughCutter':
        """WheelRoughCutter: 'WheelRoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelRoughCutter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
