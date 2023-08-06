"""_6707.py

UnbalancedMassHarmonicLoadData
"""


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.math_utility import _1310, _1320
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.system_model.analyses_and_results.static_loads import _6680
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'UnbalancedMassHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassHarmonicLoadData',)


class UnbalancedMassHarmonicLoadData(_6680.SpeedDependentHarmonicLoadData):
    """UnbalancedMassHarmonicLoadData

    This is a mastapy class.
    """

    TYPE = _UNBALANCED_MASS_HARMONIC_LOAD_DATA

    def __init__(self, instance_to_wrap: 'UnbalancedMassHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def degree_of_freedom(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom':
        """enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom: 'DegreeOfFreedom' is the original name of this property."""

        temp = self.wrapped.DegreeOfFreedom

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @degree_of_freedom.setter
    def degree_of_freedom(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DegreeOfFreedom = value

    @property
    def excitations(self) -> 'List[_1320.FourierSeries]':
        """List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Excitations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
