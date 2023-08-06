"""_808.py

GearMeshLoadDistributionAtRotation
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.ltca import _815, _809
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_LOAD_DISTRIBUTION_AT_ROTATION = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearMeshLoadDistributionAtRotation')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshLoadDistributionAtRotation',)


class GearMeshLoadDistributionAtRotation(_0.APIBase):
    """GearMeshLoadDistributionAtRotation

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_LOAD_DISTRIBUTION_AT_ROTATION

    def __init__(self, instance_to_wrap: 'GearMeshLoadDistributionAtRotation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def index(self) -> 'int':
        """int: 'Index' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Index

        if temp is None:
            return None

        return temp

    @property
    def mesh_stiffness(self) -> 'float':
        """float: 'MeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshStiffness

        if temp is None:
            return None

        return temp

    @property
    def number_of_loaded_teeth(self) -> 'int':
        """int: 'NumberOfLoadedTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfLoadedTeeth

        if temp is None:
            return None

        return temp

    @property
    def number_of_potentially_loaded_teeth(self) -> 'int':
        """int: 'NumberOfPotentiallyLoadedTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfPotentiallyLoadedTeeth

        if temp is None:
            return None

        return temp

    @property
    def transmission_error(self) -> 'float':
        """float: 'TransmissionError' is the original name of this property."""

        temp = self.wrapped.TransmissionError

        if temp is None:
            return None

        return temp

    @transmission_error.setter
    def transmission_error(self, value: 'float'):
        self.wrapped.TransmissionError = float(value) if value else 0.0

    @property
    def gear_a_in_mesh(self) -> '_815.MeshedGearLoadDistributionAnalysisAtRotation':
        """MeshedGearLoadDistributionAnalysisAtRotation: 'GearAInMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearAInMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_in_mesh(self) -> '_815.MeshedGearLoadDistributionAnalysisAtRotation':
        """MeshedGearLoadDistributionAnalysisAtRotation: 'GearBInMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBInMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_contact_lines(self) -> 'List[_809.GearMeshLoadedContactLine]':
        """List[GearMeshLoadedContactLine]: 'LoadedContactLines' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedContactLines

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshed_gears(self) -> 'List[_815.MeshedGearLoadDistributionAnalysisAtRotation]':
        """List[MeshedGearLoadDistributionAnalysisAtRotation]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshedGears

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
