"""_7001.py

AdvancedSystemDeflectionOptions
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model.gears import _2281
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.ltca import _816
from mastapy.system_model.analyses_and_results import _2433
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ADVANCED_SYSTEM_DEFLECTION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AdvancedSystemDeflectionOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionOptions',)


class AdvancedSystemDeflectionOptions(_0.APIBase):
    """AdvancedSystemDeflectionOptions

    This is a mastapy class.
    """

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_OPTIONS

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_pitch_error(self) -> 'bool':
        """bool: 'IncludePitchError' is the original name of this property."""

        temp = self.wrapped.IncludePitchError

        if temp is None:
            return None

        return temp

    @include_pitch_error.setter
    def include_pitch_error(self, value: 'bool'):
        self.wrapped.IncludePitchError = bool(value) if value else False

    @property
    def run_for_single_gear_set(self) -> 'bool':
        """bool: 'RunForSingleGearSet' is the original name of this property."""

        temp = self.wrapped.RunForSingleGearSet

        if temp is None:
            return None

        return temp

    @run_for_single_gear_set.setter
    def run_for_single_gear_set(self, value: 'bool'):
        self.wrapped.RunForSingleGearSet = bool(value) if value else False

    @property
    def seed_analysis(self) -> 'bool':
        """bool: 'SeedAnalysis' is the original name of this property."""

        temp = self.wrapped.SeedAnalysis

        if temp is None:
            return None

        return temp

    @seed_analysis.setter
    def seed_analysis(self, value: 'bool'):
        self.wrapped.SeedAnalysis = bool(value) if value else False

    @property
    def specified_gear_set(self) -> 'list_with_selected_item.ListWithSelectedItem_GearSet':
        """list_with_selected_item.ListWithSelectedItem_GearSet: 'SpecifiedGearSet' is the original name of this property."""

        temp = self.wrapped.SpecifiedGearSet

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_GearSet)(temp) if temp is not None else None

    @specified_gear_set.setter
    def specified_gear_set(self, value: 'list_with_selected_item.ListWithSelectedItem_GearSet.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_GearSet.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_GearSet.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SpecifiedGearSet = value

    @property
    def total_number_of_time_steps(self) -> 'int':
        """int: 'TotalNumberOfTimeSteps' is the original name of this property."""

        temp = self.wrapped.TotalNumberOfTimeSteps

        if temp is None:
            return None

        return temp

    @total_number_of_time_steps.setter
    def total_number_of_time_steps(self, value: 'int'):
        self.wrapped.TotalNumberOfTimeSteps = int(value) if value else 0

    @property
    def use_advanced_ltca(self) -> '_816.UseAdvancedLTCAOptions':
        """UseAdvancedLTCAOptions: 'UseAdvancedLTCA' is the original name of this property."""

        temp = self.wrapped.UseAdvancedLTCA

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_816.UseAdvancedLTCAOptions)(value) if value is not None else None

    @use_advanced_ltca.setter
    def use_advanced_ltca(self, value: '_816.UseAdvancedLTCAOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.UseAdvancedLTCA = value

    @property
    def use_data_logger(self) -> 'bool':
        """bool: 'UseDataLogger' is the original name of this property."""

        temp = self.wrapped.UseDataLogger

        if temp is None:
            return None

        return temp

    @use_data_logger.setter
    def use_data_logger(self, value: 'bool'):
        self.wrapped.UseDataLogger = bool(value) if value else False

    @property
    def time_options(self) -> '_2433.TimeOptions':
        """TimeOptions: 'TimeOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
