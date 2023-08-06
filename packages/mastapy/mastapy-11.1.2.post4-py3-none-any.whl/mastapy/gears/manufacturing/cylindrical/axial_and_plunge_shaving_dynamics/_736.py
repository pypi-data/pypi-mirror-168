"""_736.py

ShavingDynamicsViewModel
"""


from typing import List, Generic, TypeVar

from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _715, _732, _718, _719,
    _724, _725, _727, _737,
    _731
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _988, _1040
from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsViewModel',)


T = TypeVar('T', bound='_731.ShavingDynamics')


class ShavingDynamicsViewModel(_737.ShavingDynamicsViewModelBase, Generic[T]):
    """ShavingDynamicsViewModel

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _SHAVING_DYNAMICS_VIEW_MODEL

    def __init__(self, instance_to_wrap: 'ShavingDynamicsViewModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_profile_range_calculation_source(self) -> '_715.ActiveProfileRangeCalculationSource':
        """ActiveProfileRangeCalculationSource: 'ActiveProfileRangeCalculationSource' is the original name of this property."""

        temp = self.wrapped.ActiveProfileRangeCalculationSource

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_715.ActiveProfileRangeCalculationSource)(value) if value is not None else None

    @active_profile_range_calculation_source.setter
    def active_profile_range_calculation_source(self, value: '_715.ActiveProfileRangeCalculationSource'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ActiveProfileRangeCalculationSource = value

    @property
    def chart_display_method(self) -> '_988.CylindricalGearProfileMeasurementType':
        """CylindricalGearProfileMeasurementType: 'ChartDisplayMethod' is the original name of this property."""

        temp = self.wrapped.ChartDisplayMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_988.CylindricalGearProfileMeasurementType)(value) if value is not None else None

    @chart_display_method.setter
    def chart_display_method(self, value: '_988.CylindricalGearProfileMeasurementType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChartDisplayMethod = value

    @property
    def redressing_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'RedressingChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RedressingChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast redressing_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_measurement_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThicknessType':
        """enum_with_selected_value.EnumWithSelectedValue_ThicknessType: 'SelectedMeasurementMethod' is the original name of this property."""

        temp = self.wrapped.SelectedMeasurementMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThicknessType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @selected_measurement_method.setter
    def selected_measurement_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThicknessType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThicknessType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.SelectedMeasurementMethod = value

    @property
    def shaver_tip_diameter_adjustment(self) -> 'float':
        """float: 'ShaverTipDiameterAdjustment' is the original name of this property."""

        temp = self.wrapped.ShaverTipDiameterAdjustment

        if temp is None:
            return None

        return temp

    @shaver_tip_diameter_adjustment.setter
    def shaver_tip_diameter_adjustment(self, value: 'float'):
        self.wrapped.ShaverTipDiameterAdjustment = float(value) if value else 0.0

    @property
    def use_shaver_from_database(self) -> 'bool':
        """bool: 'UseShaverFromDatabase' is the original name of this property."""

        temp = self.wrapped.UseShaverFromDatabase

        if temp is None:
            return None

        return temp

    @use_shaver_from_database.setter
    def use_shaver_from_database(self, value: 'bool'):
        self.wrapped.UseShaverFromDatabase = bool(value) if value else False

    @property
    def calculation(self) -> '_732.ShavingDynamicsCalculation[T]':
        """ShavingDynamicsCalculation[T]: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Calculation

        if temp is None:
            return None

        if _732.ShavingDynamicsCalculation[T].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast calculation to ShavingDynamicsCalculation[T]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp) if temp is not None else None

    @property
    def calculation_of_type_conventional_shaving_dynamics_calculation_for_designed_gears(self) -> '_718.ConventionalShavingDynamicsCalculationForDesignedGears':
        """ConventionalShavingDynamicsCalculationForDesignedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Calculation

        if temp is None:
            return None

        if _718.ConventionalShavingDynamicsCalculationForDesignedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast calculation to ConventionalShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def calculation_of_type_conventional_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_719.ConventionalShavingDynamicsCalculationForHobbedGears':
        """ConventionalShavingDynamicsCalculationForHobbedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Calculation

        if temp is None:
            return None

        if _719.ConventionalShavingDynamicsCalculationForHobbedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast calculation to ConventionalShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def calculation_of_type_plunge_shaving_dynamics_calculation_for_designed_gears(self) -> '_724.PlungeShavingDynamicsCalculationForDesignedGears':
        """PlungeShavingDynamicsCalculationForDesignedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Calculation

        if temp is None:
            return None

        if _724.PlungeShavingDynamicsCalculationForDesignedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast calculation to PlungeShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def calculation_of_type_plunge_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_725.PlungeShavingDynamicsCalculationForHobbedGears':
        """PlungeShavingDynamicsCalculationForHobbedGears: 'Calculation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Calculation

        if temp is None:
            return None

        if _725.PlungeShavingDynamicsCalculationForHobbedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast calculation to PlungeShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def redressing_settings(self) -> 'List[_727.RedressingSettings[T]]':
        """List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RedressingSettings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def add_shaver_to_database(self):
        """ 'AddShaverToDatabase' is the original name of this method."""

        self.wrapped.AddShaverToDatabase()

    def calculate(self):
        """ 'Calculate' is the original name of this method."""

        self.wrapped.Calculate()
