"""_6725.py

PointLoadInputOptions
"""


from mastapy.math_utility import _1298
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6716
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _2221
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility_gui import _1622
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'PointLoadInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadInputOptions',)


class PointLoadInputOptions(_1622.ColumnInputOptions):
    """PointLoadInputOptions

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_INPUT_OPTIONS

    def __init__(self, instance_to_wrap: 'PointLoadInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axis(self) -> '_1298.Axis':
        """Axis: 'Axis' is the original name of this property."""

        temp = self.wrapped.Axis

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1298.Axis)(value) if value is not None else None

    @axis.setter
    def axis(self, value: '_1298.Axis'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Axis = value

    @property
    def conversion_to_load_case(self) -> '_6716.AdditionalForcesObtainedFrom':
        """AdditionalForcesObtainedFrom: 'ConversionToLoadCase' is the original name of this property."""

        temp = self.wrapped.ConversionToLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6716.AdditionalForcesObtainedFrom)(value) if value is not None else None

    @conversion_to_load_case.setter
    def conversion_to_load_case(self, value: '_6716.AdditionalForcesObtainedFrom'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ConversionToLoadCase = value

    @property
    def point_load(self) -> 'list_with_selected_item.ListWithSelectedItem_PointLoad':
        """list_with_selected_item.ListWithSelectedItem_PointLoad: 'PointLoad' is the original name of this property."""

        temp = self.wrapped.PointLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_PointLoad)(temp) if temp is not None else None

    @point_load.setter
    def point_load(self, value: 'list_with_selected_item.ListWithSelectedItem_PointLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PointLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PointLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.PointLoad = value
