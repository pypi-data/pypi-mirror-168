"""_6664.py

PointLoadHarmonicLoadData
"""


from typing import List

from mastapy.math_utility import _1310, _1320
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.static_loads import _6680
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PointLoadHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadHarmonicLoadData',)


class PointLoadHarmonicLoadData(_6680.SpeedDependentHarmonicLoadData):
    """PointLoadHarmonicLoadData

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_HARMONIC_LOAD_DATA

    def __init__(self, instance_to_wrap: 'PointLoadHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def degree_of_freedom(self) -> '_1310.DegreesOfFreedom':
        """DegreesOfFreedom: 'DegreeOfFreedom' is the original name of this property."""

        temp = self.wrapped.DegreeOfFreedom

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1310.DegreesOfFreedom)(value) if value is not None else None

    @degree_of_freedom.setter
    def degree_of_freedom(self, value: '_1310.DegreesOfFreedom'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DegreeOfFreedom = value

    @property
    def reference_shaft(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'ReferenceShaft' is the original name of this property."""

        temp = self.wrapped.ReferenceShaft

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @reference_shaft.setter
    def reference_shaft(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.ReferenceShaft = value

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
