"""_6647.py

MassDiscLoadCase
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2212
from mastapy.system_model.analyses_and_results.static_loads import _6709
from mastapy._internal.python_net import python_net_import

_MASS_DISC_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MassDiscLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscLoadCase',)


class MassDiscLoadCase(_6709.VirtualComponentLoadCase):
    """MassDiscLoadCase

    This is a mastapy class.
    """

    TYPE = _MASS_DISC_LOAD_CASE

    def __init__(self, instance_to_wrap: 'MassDiscLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mass(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Mass' is the original name of this property."""

        temp = self.wrapped.Mass

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @mass.setter
    def mass(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Mass = value

    @property
    def number_of_nodes_for_node_model(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfNodesForNodeModel' is the original name of this property."""

        temp = self.wrapped.NumberOfNodesForNodeModel

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_nodes_for_node_model.setter
    def number_of_nodes_for_node_model(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfNodesForNodeModel = value

    @property
    def polar_inertia(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PolarInertia' is the original name of this property."""

        temp = self.wrapped.PolarInertia

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @polar_inertia.setter
    def polar_inertia(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PolarInertia = value

    @property
    def transverse_inertia(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TransverseInertia' is the original name of this property."""

        temp = self.wrapped.TransverseInertia

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @transverse_inertia.setter
    def transverse_inertia(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TransverseInertia = value

    @property
    def component_design(self) -> '_2212.MassDisc':
        """MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[MassDiscLoadCase]':
        """List[MassDiscLoadCase]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
