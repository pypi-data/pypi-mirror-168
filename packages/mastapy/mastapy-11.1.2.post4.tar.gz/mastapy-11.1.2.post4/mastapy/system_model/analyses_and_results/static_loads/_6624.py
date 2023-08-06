"""_6624.py

HarmonicLoadDataExcelImport
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.utility.units_and_measurements import _1411
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.static_loads import _6652, _6626, _6602
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_EXCEL_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataExcelImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataExcelImport',)


class HarmonicLoadDataExcelImport(_6626.HarmonicLoadDataImportBase['_6602.ElectricMachineHarmonicLoadExcelImportOptions']):
    """HarmonicLoadDataExcelImport

    This is a mastapy class.
    """

    TYPE = _HARMONIC_LOAD_DATA_EXCEL_IMPORT

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataExcelImport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def column_index_of_first_data_point(self) -> 'int':
        """int: 'ColumnIndexOfFirstDataPoint' is the original name of this property."""

        temp = self.wrapped.ColumnIndexOfFirstDataPoint

        if temp is None:
            return None

        return temp

    @column_index_of_first_data_point.setter
    def column_index_of_first_data_point(self, value: 'int'):
        self.wrapped.ColumnIndexOfFirstDataPoint = int(value) if value else 0

    @property
    def column_index_of_first_speed_point(self) -> 'int':
        """int: 'ColumnIndexOfFirstSpeedPoint' is the original name of this property."""

        temp = self.wrapped.ColumnIndexOfFirstSpeedPoint

        if temp is None:
            return None

        return temp

    @column_index_of_first_speed_point.setter
    def column_index_of_first_speed_point(self, value: 'int'):
        self.wrapped.ColumnIndexOfFirstSpeedPoint = int(value) if value else 0

    @property
    def excitation_order_as_rotational_order_of_shaft(self) -> 'float':
        """float: 'ExcitationOrderAsRotationalOrderOfShaft' is the original name of this property."""

        temp = self.wrapped.ExcitationOrderAsRotationalOrderOfShaft

        if temp is None:
            return None

        return temp

    @excitation_order_as_rotational_order_of_shaft.setter
    def excitation_order_as_rotational_order_of_shaft(self, value: 'float'):
        self.wrapped.ExcitationOrderAsRotationalOrderOfShaft = float(value) if value else 0.0

    @property
    def force_units(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'ForceUnits' is the original name of this property."""

        temp = self.wrapped.ForceUnits

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @force_units.setter
    def force_units(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ForceUnits = value

    @property
    def number_of_speeds(self) -> 'int':
        """int: 'NumberOfSpeeds' is the original name of this property."""

        temp = self.wrapped.NumberOfSpeeds

        if temp is None:
            return None

        return temp

    @number_of_speeds.setter
    def number_of_speeds(self, value: 'int'):
        self.wrapped.NumberOfSpeeds = int(value) if value else 0

    @property
    def read_speeds_from_excel_sheet(self) -> 'bool':
        """bool: 'ReadSpeedsFromExcelSheet' is the original name of this property."""

        temp = self.wrapped.ReadSpeedsFromExcelSheet

        if temp is None:
            return None

        return temp

    @read_speeds_from_excel_sheet.setter
    def read_speeds_from_excel_sheet(self, value: 'bool'):
        self.wrapped.ReadSpeedsFromExcelSheet = bool(value) if value else False

    @property
    def row_index_of_first_data_point(self) -> 'int':
        """int: 'RowIndexOfFirstDataPoint' is the original name of this property."""

        temp = self.wrapped.RowIndexOfFirstDataPoint

        if temp is None:
            return None

        return temp

    @row_index_of_first_data_point.setter
    def row_index_of_first_data_point(self, value: 'int'):
        self.wrapped.RowIndexOfFirstDataPoint = int(value) if value else 0

    @property
    def row_index_of_first_speed_point(self) -> 'int':
        """int: 'RowIndexOfFirstSpeedPoint' is the original name of this property."""

        temp = self.wrapped.RowIndexOfFirstSpeedPoint

        if temp is None:
            return None

        return temp

    @row_index_of_first_speed_point.setter
    def row_index_of_first_speed_point(self, value: 'int'):
        self.wrapped.RowIndexOfFirstSpeedPoint = int(value) if value else 0

    @property
    def row_index_of_last_data_point(self) -> 'int':
        """int: 'RowIndexOfLastDataPoint' is the original name of this property."""

        temp = self.wrapped.RowIndexOfLastDataPoint

        if temp is None:
            return None

        return temp

    @row_index_of_last_data_point.setter
    def row_index_of_last_data_point(self, value: 'int'):
        self.wrapped.RowIndexOfLastDataPoint = int(value) if value else 0

    @property
    def sheet_for_first_set_of_data(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'SheetForFirstSetOfData' is the original name of this property."""

        temp = self.wrapped.SheetForFirstSetOfData

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @sheet_for_first_set_of_data.setter
    def sheet_for_first_set_of_data(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.SheetForFirstSetOfData = value

    @property
    def sheet_with_speed_data(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'SheetWithSpeedData' is the original name of this property."""

        temp = self.wrapped.SheetWithSpeedData

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @sheet_with_speed_data.setter
    def sheet_with_speed_data(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.SheetWithSpeedData = value

    @property
    def speed_units(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'SpeedUnits' is the original name of this property."""

        temp = self.wrapped.SpeedUnits

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @speed_units.setter
    def speed_units(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SpeedUnits = value

    @property
    def torque_units(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'TorqueUnits' is the original name of this property."""

        temp = self.wrapped.TorqueUnits

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @torque_units.setter
    def torque_units(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.TorqueUnits = value

    @property
    def speeds(self) -> 'List[_6652.NamedSpeed]':
        """List[NamedSpeed]: 'Speeds' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Speeds

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def select_excel_file(self):
        """ 'SelectExcelFile' is the original name of this method."""

        self.wrapped.SelectExcelFile()
