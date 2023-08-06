"""_2156.py

RaceBearingFE
"""


from typing import List

from mastapy.system_model.fe import _2108, _2115
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _2199
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RACE_BEARING_FE = python_net_import('SMT.MastaAPI.SystemModel.FE', 'RaceBearingFE')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceBearingFE',)


class RaceBearingFE(_0.APIBase):
    """RaceBearingFE

    This is a mastapy class.
    """

    TYPE = _RACE_BEARING_FE

    def __init__(self, instance_to_wrap: 'RaceBearingFE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def alignment_method(self) -> '_2108.AlignmentMethodForRaceBearing':
        """AlignmentMethodForRaceBearing: 'AlignmentMethod' is the original name of this property."""

        temp = self.wrapped.AlignmentMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2108.AlignmentMethodForRaceBearing)(value) if value is not None else None

    @alignment_method.setter
    def alignment_method(self, value: '_2108.AlignmentMethodForRaceBearing'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentMethod = value

    @property
    def datum(self) -> 'list_with_selected_item.ListWithSelectedItem_Datum':
        """list_with_selected_item.ListWithSelectedItem_Datum: 'Datum' is the original name of this property."""

        temp = self.wrapped.Datum

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Datum)(temp) if temp is not None else None

    @datum.setter
    def datum(self, value: 'list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Datum.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.Datum = value

    @property
    def fe_filename(self) -> 'str':
        """str: 'FEFilename' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEFilename

        if temp is None:
            return None

        return temp

    @property
    def links(self) -> 'List[_2115.BearingRaceNodeLink]':
        """List[BearingRaceNodeLink]: 'Links' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Links

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def copy_datum_to_manual(self):
        """ 'CopyDatumToManual' is the original name of this method."""

        self.wrapped.CopyDatumToManual()

    def find_nodes_for_links(self):
        """ 'FindNodesForLinks' is the original name of this method."""

        self.wrapped.FindNodesForLinks()

    def import_fe_mesh(self):
        """ 'ImportFEMesh' is the original name of this method."""

        self.wrapped.ImportFEMesh()

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
