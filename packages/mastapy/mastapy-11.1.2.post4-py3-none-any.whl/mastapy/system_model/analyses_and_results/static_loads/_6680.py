"""_6680.py

SpeedDependentHarmonicLoadData
"""


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6622
from mastapy._internal.python_net import python_net_import

_SPEED_DEPENDENT_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpeedDependentHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('SpeedDependentHarmonicLoadData',)


class SpeedDependentHarmonicLoadData(_6622.HarmonicLoadDataBase):
    """SpeedDependentHarmonicLoadData

    This is a mastapy class.
    """

    TYPE = _SPEED_DEPENDENT_HARMONIC_LOAD_DATA

    def __init__(self, instance_to_wrap: 'SpeedDependentHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_speed(self) -> 'list_with_selected_item.ListWithSelectedItem_float':
        """list_with_selected_item.ListWithSelectedItem_float: 'SelectedSpeed' is the original name of this property."""

        temp = self.wrapped.SelectedSpeed

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_float)(temp) if temp is not None else None

    @selected_speed.setter
    def selected_speed(self, value: 'list_with_selected_item.ListWithSelectedItem_float.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_float.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0)
        self.wrapped.SelectedSpeed = value

    @property
    def show_all_speeds(self) -> 'bool':
        """bool: 'ShowAllSpeeds' is the original name of this property."""

        temp = self.wrapped.ShowAllSpeeds

        if temp is None:
            return None

        return temp

    @show_all_speeds.setter
    def show_all_speeds(self, value: 'bool'):
        self.wrapped.ShowAllSpeeds = bool(value) if value else False
