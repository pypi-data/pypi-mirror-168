"""_810.py

GearMeshLoadedContactPoint
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_LOADED_CONTACT_POINT = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearMeshLoadedContactPoint')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshLoadedContactPoint',)


class GearMeshLoadedContactPoint(_0.APIBase):
    """GearMeshLoadedContactPoint

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_LOADED_CONTACT_POINT

    def __init__(self, instance_to_wrap: 'GearMeshLoadedContactPoint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_line_index(self) -> 'int':
        """int: 'ContactLineIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLineIndex

        if temp is None:
            return None

        return temp

    @property
    def contact_point_index(self) -> 'int':
        """int: 'ContactPointIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactPointIndex

        if temp is None:
            return None

        return temp

    @property
    def contact_pressure(self) -> 'float':
        """float: 'ContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactPressure

        if temp is None:
            return None

        return temp

    @property
    def depth_of_max_sheer_stress(self) -> 'float':
        """float: 'DepthOfMaxSheerStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaxSheerStress

        if temp is None:
            return None

        return temp

    @property
    def force_unit_length(self) -> 'float':
        """float: 'ForceUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceUnitLength

        if temp is None:
            return None

        return temp

    @property
    def gaps_between_flanks_in_transverse_plane(self) -> 'float':
        """float: 'GapsBetweenFlanksInTransversePlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GapsBetweenFlanksInTransversePlane

        if temp is None:
            return None

        return temp

    @property
    def hertzian_contact_half_width(self) -> 'float':
        """float: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactHalfWidth

        if temp is None:
            return None

        return temp

    @property
    def max_sheer_stress(self) -> 'float':
        """float: 'MaxSheerStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxSheerStress

        if temp is None:
            return None

        return temp

    @property
    def mesh_position_index(self) -> 'int':
        """int: 'MeshPositionIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshPositionIndex

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def strip_length(self) -> 'float':
        """float: 'StripLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StripLength

        if temp is None:
            return None

        return temp

    @property
    def total_deflection_for_mesh(self) -> 'float':
        """float: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalDeflectionForMesh

        if temp is None:
            return None

        return temp

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
