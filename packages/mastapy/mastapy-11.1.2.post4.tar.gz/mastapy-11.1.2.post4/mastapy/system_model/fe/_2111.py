"""_2111.py

BaseFEWithSelection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses import (
    _166, _159, _174, _173
)
from mastapy.system_model.part_model import _2195
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BASE_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'BaseFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('BaseFEWithSelection',)


class BaseFEWithSelection(_0.APIBase):
    """BaseFEWithSelection

    This is a mastapy class.
    """

    TYPE = _BASE_FE_WITH_SELECTION

    def __init__(self, instance_to_wrap: 'BaseFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_selected_faces(self) -> 'int':
        """int: 'NumberOfSelectedFaces' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfSelectedFaces

        if temp is None:
            return None

        return temp

    @property
    def number_of_selected_nodes(self) -> 'int':
        """int: 'NumberOfSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfSelectedNodes

        if temp is None:
            return None

        return temp

    @property
    def selected_component(self) -> 'str':
        """str: 'SelectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedComponent

        if temp is None:
            return None

        return temp

    @property
    def component_draw_style(self) -> '_166.FEModelComponentDrawStyle':
        """FEModelComponentDrawStyle: 'ComponentDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDrawStyle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def draw_style(self) -> '_159.DrawStyleForFE':
        """DrawStyleForFE: 'DrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DrawStyle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def node_selection(self) -> '_174.FENodeSelectionDrawStyle':
        """FENodeSelectionDrawStyle: 'NodeSelection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeSelection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def transparency_draw_style(self) -> '_173.FEModelTransparencyDrawStyle':
        """FEModelTransparencyDrawStyle: 'TransparencyDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransparencyDrawStyle

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

    def select_component(self, component: '_2195.Component'):
        """ 'SelectComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)
        """

        self.wrapped.SelectComponent(component.wrapped if component else None)

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
