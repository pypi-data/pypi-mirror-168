"""_2312.py

SuperchargerRotorSet
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility_gui.charts import _1632
from mastapy.system_model.part_model.gears.supercharger_rotor_set import (
    _2314, _2304, _2307, _2305,
    _2306, _2309, _2308
)
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_SUPERCHARGER_ROTOR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'SuperchargerRotorSet')


__docformat__ = 'restructuredtext en'
__all__ = ('SuperchargerRotorSet',)


class SuperchargerRotorSet(_1605.NamedDatabaseItem):
    """SuperchargerRotorSet

    This is a mastapy class.
    """

    TYPE = _SUPERCHARGER_ROTOR_SET

    def __init__(self, instance_to_wrap: 'SuperchargerRotorSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_reaction_force(self) -> 'float':
        """float: 'AxialReactionForce' is the original name of this property."""

        temp = self.wrapped.AxialReactionForce

        if temp is None:
            return None

        return temp

    @axial_reaction_force.setter
    def axial_reaction_force(self, value: 'float'):
        self.wrapped.AxialReactionForce = float(value) if value else 0.0

    @property
    def dynamic_load_factor(self) -> 'float':
        """float: 'DynamicLoadFactor' is the original name of this property."""

        temp = self.wrapped.DynamicLoadFactor

        if temp is None:
            return None

        return temp

    @dynamic_load_factor.setter
    def dynamic_load_factor(self, value: 'float'):
        self.wrapped.DynamicLoadFactor = float(value) if value else 0.0

    @property
    def lateral_reaction_force(self) -> 'float':
        """float: 'LateralReactionForce' is the original name of this property."""

        temp = self.wrapped.LateralReactionForce

        if temp is None:
            return None

        return temp

    @lateral_reaction_force.setter
    def lateral_reaction_force(self, value: 'float'):
        self.wrapped.LateralReactionForce = float(value) if value else 0.0

    @property
    def lateral_reaction_moment(self) -> 'float':
        """float: 'LateralReactionMoment' is the original name of this property."""

        temp = self.wrapped.LateralReactionMoment

        if temp is None:
            return None

        return temp

    @lateral_reaction_moment.setter
    def lateral_reaction_moment(self, value: 'float'):
        self.wrapped.LateralReactionMoment = float(value) if value else 0.0

    @property
    def selected_file_name(self) -> 'str':
        """str: 'SelectedFileName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedFileName

        if temp is None:
            return None

        return temp

    @property
    def supercharger_map_chart(self) -> '_1632.ThreeDChartDefinition':
        """ThreeDChartDefinition: 'SuperchargerMapChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SuperchargerMapChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def vertical_reaction_force(self) -> 'float':
        """float: 'VerticalReactionForce' is the original name of this property."""

        temp = self.wrapped.VerticalReactionForce

        if temp is None:
            return None

        return temp

    @vertical_reaction_force.setter
    def vertical_reaction_force(self, value: 'float'):
        self.wrapped.VerticalReactionForce = float(value) if value else 0.0

    @property
    def vertical_reaction_moment(self) -> 'float':
        """float: 'VerticalReactionMoment' is the original name of this property."""

        temp = self.wrapped.VerticalReactionMoment

        if temp is None:
            return None

        return temp

    @vertical_reaction_moment.setter
    def vertical_reaction_moment(self, value: 'float'):
        self.wrapped.VerticalReactionMoment = float(value) if value else 0.0

    @property
    def y_variable_for_imported_data(self) -> '_2314.YVariableForImportedData':
        """YVariableForImportedData: 'YVariableForImportedData' is the original name of this property."""

        temp = self.wrapped.YVariableForImportedData

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2314.YVariableForImportedData)(value) if value is not None else None

    @y_variable_for_imported_data.setter
    def y_variable_for_imported_data(self, value: '_2314.YVariableForImportedData'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.YVariableForImportedData = value

    @property
    def boost_pressure(self) -> '_2304.BoostPressureInputOptions':
        """BoostPressureInputOptions: 'BoostPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoostPressure

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def file(self) -> '_2307.RotorSetDataInputFileOptions':
        """RotorSetDataInputFileOptions: 'File' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.File

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def input_power(self) -> '_2305.InputPowerInputOptions':
        """InputPowerInputOptions: 'InputPower' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputPower

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def pressure_ratio(self) -> '_2306.PressureRatioInputOptions':
        """PressureRatioInputOptions: 'PressureRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureRatio

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rotor_speed(self) -> '_2309.RotorSpeedInputOptions':
        """RotorSpeedInputOptions: 'RotorSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotorSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def measured_points(self) -> 'List[_2308.RotorSetMeasuredPoint]':
        """List[RotorSetMeasuredPoint]: 'MeasuredPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasuredPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def select_different_file(self):
        """ 'SelectDifferentFile' is the original name of this method."""

        self.wrapped.SelectDifferentFile()
