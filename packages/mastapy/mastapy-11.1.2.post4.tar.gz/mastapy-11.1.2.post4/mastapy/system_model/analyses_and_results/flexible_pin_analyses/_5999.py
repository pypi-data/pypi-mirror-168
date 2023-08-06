"""_5999.py

FlexiblePinAnalysisOptions
"""


from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _6528, _6535
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4127
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.load_case_groups import _5398
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisOptions',)


class FlexiblePinAnalysisOptions(_0.APIBase):
    """FlexiblePinAnalysisOptions

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ANALYSIS_OPTIONS

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def extreme_load_case(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        """list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'ExtremeLoadCase' is the original name of this property."""

        temp = self.wrapped.ExtremeLoadCase

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(temp) if temp is not None else None

    @extreme_load_case.setter
    def extreme_load_case(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ExtremeLoadCase = value

    @property
    def extreme_load_case_for_stop_start(self) -> '_6528.StaticLoadCase':
        """StaticLoadCase: 'ExtremeLoadCaseForStopStart' is the original name of this property."""

        temp = self.wrapped.ExtremeLoadCaseForStopStart

        if temp is None:
            return None

        if _6528.StaticLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast extreme_load_case_for_stop_start to StaticLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @extreme_load_case_for_stop_start.setter
    def extreme_load_case_for_stop_start(self, value: '_6528.StaticLoadCase'):
        value = value.wrapped if value else None
        self.wrapped.ExtremeLoadCaseForStopStart = value

    @property
    def include_flexible_bearing_races(self) -> 'bool':
        """bool: 'IncludeFlexibleBearingRaces' is the original name of this property."""

        temp = self.wrapped.IncludeFlexibleBearingRaces

        if temp is None:
            return None

        return temp

    @include_flexible_bearing_races.setter
    def include_flexible_bearing_races(self, value: 'bool'):
        self.wrapped.IncludeFlexibleBearingRaces = bool(value) if value else False

    @property
    def ldd(self) -> 'list_with_selected_item.ListWithSelectedItem_DutyCycle':
        """list_with_selected_item.ListWithSelectedItem_DutyCycle: 'LDD' is the original name of this property."""

        temp = self.wrapped.LDD

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_DutyCycle)(temp) if temp is not None else None

    @ldd.setter
    def ldd(self, value: 'list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_DutyCycle.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.LDD = value

    @property
    def nominal_load_case(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        """list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'NominalLoadCase' is the original name of this property."""

        temp = self.wrapped.NominalLoadCase

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(temp) if temp is not None else None

    @nominal_load_case.setter
    def nominal_load_case(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.NominalLoadCase = value

    @property
    def nominal_load_case_for_stop_start(self) -> '_6528.StaticLoadCase':
        """StaticLoadCase: 'NominalLoadCaseForStopStart' is the original name of this property."""

        temp = self.wrapped.NominalLoadCaseForStopStart

        if temp is None:
            return None

        if _6528.StaticLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast nominal_load_case_for_stop_start to StaticLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @nominal_load_case_for_stop_start.setter
    def nominal_load_case_for_stop_start(self, value: '_6528.StaticLoadCase'):
        value = value.wrapped if value else None
        self.wrapped.NominalLoadCaseForStopStart = value
