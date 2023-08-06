"""_6611.py

FEPartLoadCase
"""


from typing import List

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.fe import _2110, _2133
from mastapy.system_model.part_model import _2203
from mastapy.system_model.analyses_and_results.static_loads import _6532
from mastapy._internal.python_net import python_net_import

_FE_PART_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FEPartLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartLoadCase',)


class FEPartLoadCase(_6532.AbstractShaftOrHousingLoadCase):
    """FEPartLoadCase

    This is a mastapy class.
    """

    TYPE = _FE_PART_LOAD_CASE

    def __init__(self, instance_to_wrap: 'FEPartLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_angle_index(self) -> 'list_with_selected_item.ListWithSelectedItem_int':
        """list_with_selected_item.ListWithSelectedItem_int: 'ActiveAngleIndex' is the original name of this property."""

        temp = self.wrapped.ActiveAngleIndex

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_int)(temp) if temp is not None else None

    @active_angle_index.setter
    def active_angle_index(self, value: 'list_with_selected_item.ListWithSelectedItem_int.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0)
        self.wrapped.ActiveAngleIndex = value

    @property
    def angle(self) -> 'float':
        """float: 'Angle' is the original name of this property."""

        temp = self.wrapped.Angle

        if temp is None:
            return None

        return temp

    @angle.setter
    def angle(self, value: 'float'):
        self.wrapped.Angle = float(value) if value else 0.0

    @property
    def angle_source(self) -> '_2110.AngleSource':
        """AngleSource: 'AngleSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngleSource

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2110.AngleSource)(value) if value is not None else None

    @property
    def fe_substructure(self) -> 'list_with_selected_item.ListWithSelectedItem_FESubstructure':
        """list_with_selected_item.ListWithSelectedItem_FESubstructure: 'FESubstructure' is the original name of this property."""

        temp = self.wrapped.FESubstructure

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_FESubstructure)(temp) if temp is not None else None

    @fe_substructure.setter
    def fe_substructure(self, value: 'list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FESubstructure.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.FESubstructure = value

    @property
    def mass_scaling_factor(self) -> 'float':
        """float: 'MassScalingFactor' is the original name of this property."""

        temp = self.wrapped.MassScalingFactor

        if temp is None:
            return None

        return temp

    @mass_scaling_factor.setter
    def mass_scaling_factor(self, value: 'float'):
        self.wrapped.MassScalingFactor = float(value) if value else 0.0

    @property
    def override_default_fe_substructure(self) -> 'bool':
        """bool: 'OverrideDefaultFESubstructure' is the original name of this property."""

        temp = self.wrapped.OverrideDefaultFESubstructure

        if temp is None:
            return None

        return temp

    @override_default_fe_substructure.setter
    def override_default_fe_substructure(self, value: 'bool'):
        self.wrapped.OverrideDefaultFESubstructure = bool(value) if value else False

    @property
    def stiffness_scaling_factor(self) -> 'float':
        """float: 'StiffnessScalingFactor' is the original name of this property."""

        temp = self.wrapped.StiffnessScalingFactor

        if temp is None:
            return None

        return temp

    @stiffness_scaling_factor.setter
    def stiffness_scaling_factor(self, value: 'float'):
        self.wrapped.StiffnessScalingFactor = float(value) if value else 0.0

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[FEPartLoadCase]':
        """List[FEPartLoadCase]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
