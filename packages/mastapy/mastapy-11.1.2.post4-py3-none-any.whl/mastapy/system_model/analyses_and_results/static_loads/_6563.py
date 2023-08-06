"""_6563.py

ConceptCouplingLoadCase
"""


from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.part_model import _2222
from mastapy.system_model import _1959
from mastapy.math_utility import _1341
from mastapy.system_model.part_model.couplings import _2330
from mastapy.math_utility.control import _1381
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingLoadCase',)


class ConceptCouplingLoadCase(_6576.CouplingLoadCase):
    """ConceptCouplingLoadCase

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ConceptCouplingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def efficiency(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Efficiency' is the original name of this property."""

        temp = self.wrapped.Efficiency

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @efficiency.setter
    def efficiency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Efficiency = value

    @property
    def power_load_for_reference_speed(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        """list_with_selected_item.ListWithSelectedItem_PowerLoad: 'PowerLoadForReferenceSpeed' is the original name of this property."""

        temp = self.wrapped.PowerLoadForReferenceSpeed

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_PowerLoad)(temp) if temp is not None else None

    @power_load_for_reference_speed.setter
    def power_load_for_reference_speed(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.PowerLoadForReferenceSpeed = value

    @property
    def speed_ratio(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SpeedRatio' is the original name of this property."""

        temp = self.wrapped.SpeedRatio

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @speed_ratio.setter
    def speed_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpeedRatio = value

    @property
    def speed_ratio_specification_method(self) -> '_1959.ConceptCouplingSpeedRatioSpecificationMethod':
        """ConceptCouplingSpeedRatioSpecificationMethod: 'SpeedRatioSpecificationMethod' is the original name of this property."""

        temp = self.wrapped.SpeedRatioSpecificationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1959.ConceptCouplingSpeedRatioSpecificationMethod)(value) if value is not None else None

    @speed_ratio_specification_method.setter
    def speed_ratio_specification_method(self, value: '_1959.ConceptCouplingSpeedRatioSpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpeedRatioSpecificationMethod = value

    @property
    def speed_ratio_vs_time(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'SpeedRatioVsTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedRatioVsTime

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2330.ConceptCoupling':
        """ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def speed_ratio_pid_control(self) -> '_1381.PIDControlSettings':
        """PIDControlSettings: 'SpeedRatioPIDControl' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedRatioPIDControl

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
