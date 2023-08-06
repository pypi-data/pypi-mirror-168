"""_1262.py

CycloidalDiscDesign
"""


from typing import List

from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.cycloidal import _1265
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_DESIGN = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscDesign',)


class CycloidalDiscDesign(_0.APIBase):
    """CycloidalDiscDesign

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_DESIGN

    def __init__(self, instance_to_wrap: 'CycloidalDiscDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def crowning_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'CrowningChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CrowningChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast crowning_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def disc_id(self) -> 'int':
        """int: 'DiscID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiscID

        if temp is None:
            return None

        return temp

    @property
    def estimated_modifications_from_spline_fit(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'EstimatedModificationsFromSplineFit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EstimatedModificationsFromSplineFit

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast estimated_modifications_from_spline_fit to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property."""

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def generating_wheel_centre_circle_diameter(self) -> 'float':
        """float: 'GeneratingWheelCentreCircleDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeneratingWheelCentreCircleDiameter

        if temp is None:
            return None

        return temp

    @property
    def generating_wheel_diameter(self) -> 'float':
        """float: 'GeneratingWheelDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeneratingWheelDiameter

        if temp is None:
            return None

        return temp

    @property
    def lobe_symmetry_angle_with_no_lobe_modifications(self) -> 'float':
        """float: 'LobeSymmetryAngleWithNoLobeModifications' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LobeSymmetryAngleWithNoLobeModifications

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
    def modifications_specification(self) -> '_1265.CycloidalDiscModificationsSpecification':
        """CycloidalDiscModificationsSpecification: 'ModificationsSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModificationsSpecification

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
