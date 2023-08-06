"""_1261.py

CycloidalAssemblyDesign
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.cycloidal import _1268, _1267, _1262
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_DESIGN = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalAssemblyDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyDesign',)


class CycloidalAssemblyDesign(_0.APIBase):
    """CycloidalAssemblyDesign

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_ASSEMBLY_DESIGN

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def eccentricity(self) -> 'float':
        """float: 'Eccentricity' is the original name of this property."""

        temp = self.wrapped.Eccentricity

        if temp is None:
            return None

        return temp

    @eccentricity.setter
    def eccentricity(self, value: 'float'):
        self.wrapped.Eccentricity = float(value) if value else 0.0

    @property
    def first_disc_angle(self) -> 'float':
        """float: 'FirstDiscAngle' is the original name of this property."""

        temp = self.wrapped.FirstDiscAngle

        if temp is None:
            return None

        return temp

    @first_disc_angle.setter
    def first_disc_angle(self, value: 'float'):
        self.wrapped.FirstDiscAngle = float(value) if value else 0.0

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
    def number_of_lobes(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfLobes' is the original name of this property."""

        temp = self.wrapped.NumberOfLobes

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_lobes.setter
    def number_of_lobes(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfLobes = value

    @property
    def ratio(self) -> 'float':
        """float: 'Ratio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Ratio

        if temp is None:
            return None

        return temp

    @property
    def tooth_symmetry_angle(self) -> 'float':
        """float: 'ToothSymmetryAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothSymmetryAngle

        if temp is None:
            return None

        return temp

    @property
    def ring_pins(self) -> '_1268.RingPinsDesign':
        """RingPinsDesign: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def disc_phases(self) -> 'List[_1267.NamedDiscPhase]':
        """List[NamedDiscPhase]: 'DiscPhases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiscPhases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def discs(self) -> 'List[_1262.CycloidalDiscDesign]':
        """List[CycloidalDiscDesign]: 'Discs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Discs

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
