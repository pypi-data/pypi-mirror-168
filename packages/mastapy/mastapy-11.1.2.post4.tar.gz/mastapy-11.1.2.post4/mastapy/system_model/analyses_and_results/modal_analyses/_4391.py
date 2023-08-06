"""_4391.py

ModalAnalysisBarModelFEExportOptions
"""


from typing import List, Optional

from mastapy.nodal_analysis import _49, _50
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item, enum_with_selected_value
from mastapy.system_model.part_model import _2203
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.fe_export_utility import _158
from mastapy.utility.units_and_measurements import _1411
from mastapy.nodal_analysis.dev_tools_analyses import _160
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_BAR_MODEL_FE_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysisBarModelFEExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisBarModelFEExportOptions',)


class ModalAnalysisBarModelFEExportOptions(_0.APIBase):
    """ModalAnalysisBarModelFEExportOptions

    This is a mastapy class.
    """

    TYPE = _MODAL_ANALYSIS_BAR_MODEL_FE_EXPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'ModalAnalysisBarModelFEExportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_type(self) -> '_49.BarModelAnalysisType':
        """BarModelAnalysisType: 'AnalysisType' is the original name of this property."""

        temp = self.wrapped.AnalysisType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_49.BarModelAnalysisType)(value) if value is not None else None

    @analysis_type.setter
    def analysis_type(self, value: '_49.BarModelAnalysisType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AnalysisType = value

    @property
    def connect_to_full_fe_mesh(self) -> 'bool':
        """bool: 'ConnectToFullFEMesh' is the original name of this property."""

        temp = self.wrapped.ConnectToFullFEMesh

        if temp is None:
            return None

        return temp

    @connect_to_full_fe_mesh.setter
    def connect_to_full_fe_mesh(self, value: 'bool'):
        self.wrapped.ConnectToFullFEMesh = bool(value) if value else False

    @property
    def coordinate_system(self) -> 'list_with_selected_item.ListWithSelectedItem_FEPart':
        """list_with_selected_item.ListWithSelectedItem_FEPart: 'CoordinateSystem' is the original name of this property."""

        temp = self.wrapped.CoordinateSystem

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_FEPart)(temp) if temp is not None else None

    @coordinate_system.setter
    def coordinate_system(self, value: 'list_with_selected_item.ListWithSelectedItem_FEPart.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FEPart.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FEPart.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.CoordinateSystem = value

    @property
    def error_message(self) -> 'str':
        """str: 'ErrorMessage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ErrorMessage

        if temp is None:
            return None

        return temp

    @property
    def fe_file_to_include(self) -> 'str':
        """str: 'FEFileToInclude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEFileToInclude

        if temp is None:
            return None

        return temp

    @property
    def fe_package(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat':
        """enum_with_selected_value.EnumWithSelectedValue_FEExportFormat: 'FEPackage' is the original name of this property."""

        temp = self.wrapped.FEPackage

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @fe_package.setter
    def fe_package(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.FEPackage = value

    @property
    def fe_part(self) -> 'list_with_selected_item.ListWithSelectedItem_FEPart':
        """list_with_selected_item.ListWithSelectedItem_FEPart: 'FEPart' is the original name of this property."""

        temp = self.wrapped.FEPart

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_FEPart)(temp) if temp is not None else None

    @fe_part.setter
    def fe_part(self, value: 'list_with_selected_item.ListWithSelectedItem_FEPart.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FEPart.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FEPart.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.FEPart = value

    @property
    def force_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'ForceUnit' is the original name of this property."""

        temp = self.wrapped.ForceUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @force_unit.setter
    def force_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ForceUnit = value

    @property
    def length_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'LengthUnit' is the original name of this property."""

        temp = self.wrapped.LengthUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @length_unit.setter
    def length_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.LengthUnit = value

    @property
    def shaft_export_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BarModelExportType':
        """enum_with_selected_value.EnumWithSelectedValue_BarModelExportType: 'ShaftExportType' is the original name of this property."""

        temp = self.wrapped.ShaftExportType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BarModelExportType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @shaft_export_type.setter
    def shaft_export_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BarModelExportType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BarModelExportType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ShaftExportType = value

    @property
    def use_fe_file_from_fe_substructure(self) -> 'bool':
        """bool: 'UseFEFileFromFESubstructure' is the original name of this property."""

        temp = self.wrapped.UseFEFileFromFESubstructure

        if temp is None:
            return None

        return temp

    @use_fe_file_from_fe_substructure.setter
    def use_fe_file_from_fe_substructure(self, value: 'bool'):
        self.wrapped.UseFEFileFromFESubstructure = bool(value) if value else False

    @property
    def mode_options(self) -> '_160.EigenvalueOptions':
        """EigenvalueOptions: 'ModeOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

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

    def export_to_file(self, file_path: 'str'):
        """ 'ExportToFile' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.ExportToFile(file_path if file_path else '')

    def set_fe_file_to_include(self, file_path: 'str', format_: '_158.FEExportFormat', length_scale: Optional['float'] = 1.0, force_scale: Optional['float'] = 1.0):
        """ 'SetFEFileToInclude' is the original name of this method.

        Args:
            file_path (str)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
        """

        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(format_)
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        self.wrapped.SetFEFileToInclude(file_path if file_path else '', format_, length_scale if length_scale else 0.0, force_scale if force_scale else 0.0)

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
