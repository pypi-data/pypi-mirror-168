"""_701.py

CylindricalManufacturedVirtualGearInMesh
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _713
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MANUFACTURED_VIRTUAL_GEAR_IN_MESH = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CylindricalManufacturedVirtualGearInMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalManufacturedVirtualGearInMesh',)


class CylindricalManufacturedVirtualGearInMesh(_0.APIBase):
    """CylindricalManufacturedVirtualGearInMesh

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MANUFACTURED_VIRTUAL_GEAR_IN_MESH

    def __init__(self, instance_to_wrap: 'CylindricalManufacturedVirtualGearInMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_moment_arm_for_agma_rating(self) -> 'float':
        """float: 'BendingMomentArmForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingMomentArmForAGMARating

        if temp is None:
            return None

        return temp

    @property
    def bending_moment_arm_for_iso_rating(self) -> 'float':
        """float: 'BendingMomentArmForISORating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingMomentArmForISORating

        if temp is None:
            return None

        return temp

    @property
    def form_factor_for_iso_rating(self) -> 'float':
        """float: 'FormFactorForISORating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormFactorForISORating

        if temp is None:
            return None

        return temp

    @property
    def load_direction_for_agma_rating(self) -> 'float':
        """float: 'LoadDirectionForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDirectionForAGMARating

        if temp is None:
            return None

        return temp

    @property
    def load_direction_angle_for_iso_rating(self) -> 'float':
        """float: 'LoadDirectionAngleForISORating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDirectionAngleForISORating

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
    def stress_correction_factor_for_iso_rating(self) -> 'float':
        """float: 'StressCorrectionFactorForISORating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCorrectionFactorForISORating

        if temp is None:
            return None

        return temp

    @property
    def tooth_root_chord_for_agma_rating(self) -> 'float':
        """float: 'ToothRootChordForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootChordForAGMARating

        if temp is None:
            return None

        return temp

    @property
    def virtual_gear(self) -> '_713.VirtualSimulationCalculator':
        """VirtualSimulationCalculator: 'VirtualGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualGear

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
