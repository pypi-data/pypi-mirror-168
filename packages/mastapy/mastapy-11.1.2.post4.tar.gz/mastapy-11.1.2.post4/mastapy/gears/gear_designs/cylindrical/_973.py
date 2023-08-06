"""_973.py

CylindricalGearCuttingOptions
"""


from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item
from mastapy.gears.gear_designs.cylindrical import (
    _1011, _969, _971, _985,
    _1037, _993
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical import _578
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_CUTTING_OPTIONS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearCuttingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCuttingOptions',)


class CylindricalGearCuttingOptions(_0.APIBase):
    """CylindricalGearCuttingOptions

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_CUTTING_OPTIONS

    def __init__(self, instance_to_wrap: 'CylindricalGearCuttingOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def geometry_specification_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType':
        """enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType: 'GeometrySpecificationType' is the original name of this property."""

        temp = self.wrapped.GeometrySpecificationType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @geometry_specification_type.setter
    def geometry_specification_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.GeometrySpecificationType = value

    @property
    def thickness_for_analyses(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'ThicknessForAnalyses' is the original name of this property."""

        temp = self.wrapped.ThicknessForAnalyses

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @thickness_for_analyses.setter
    def thickness_for_analyses(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.ThicknessForAnalyses = value

    @property
    def use_design_default_toleranced_measurement(self) -> 'bool':
        """bool: 'UseDesignDefaultTolerancedMeasurement' is the original name of this property."""

        temp = self.wrapped.UseDesignDefaultTolerancedMeasurement

        if temp is None:
            return None

        return temp

    @use_design_default_toleranced_measurement.setter
    def use_design_default_toleranced_measurement(self, value: 'bool'):
        self.wrapped.UseDesignDefaultTolerancedMeasurement = bool(value) if value else False

    @property
    def cylindrical_gear_cutter(self) -> '_969.CylindricalGearAbstractRack':
        """CylindricalGearAbstractRack: 'CylindricalGearCutter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearCutter

        if temp is None:
            return None

        if _969.CylindricalGearAbstractRack.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_cutter to CylindricalGearAbstractRack. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_cutter_of_type_cylindrical_gear_basic_rack(self) -> '_971.CylindricalGearBasicRack':
        """CylindricalGearBasicRack: 'CylindricalGearCutter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearCutter

        if temp is None:
            return None

        if _971.CylindricalGearBasicRack.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_cutter to CylindricalGearBasicRack. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_cutter_of_type_cylindrical_gear_pinion_type_cutter(self) -> '_985.CylindricalGearPinionTypeCutter':
        """CylindricalGearPinionTypeCutter: 'CylindricalGearCutter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearCutter

        if temp is None:
            return None

        if _985.CylindricalGearPinionTypeCutter.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_cutter to CylindricalGearPinionTypeCutter. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_cutter_of_type_standard_rack(self) -> '_1037.StandardRack':
        """StandardRack: 'CylindricalGearCutter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearCutter

        if temp is None:
            return None

        if _1037.StandardRack.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_cutter to StandardRack. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def manufacturing_configuration(self) -> '_578.CylindricalGearManufacturingConfig':
        """CylindricalGearManufacturingConfig: 'ManufacturingConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManufacturingConfiguration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def manufacturing_configuration_selection(self) -> '_993.CylindricalGearSetManufacturingConfigurationSelection':
        """CylindricalGearSetManufacturingConfigurationSelection: 'ManufacturingConfigurationSelection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManufacturingConfigurationSelection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
