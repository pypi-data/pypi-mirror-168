"""_1881.py

LoadedPlainJournalBearingRow
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.bearings import _1645
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOADED_PLAIN_JOURNAL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.FluidFilm', 'LoadedPlainJournalBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedPlainJournalBearingRow',)


class LoadedPlainJournalBearingRow(_0.APIBase):
    """LoadedPlainJournalBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_PLAIN_JOURNAL_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedPlainJournalBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_position_of_the_minimum_film_thickness_from_the_x_axis(self) -> 'float':
        """float: 'AngularPositionOfTheMinimumFilmThicknessFromTheXAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularPositionOfTheMinimumFilmThicknessFromTheXAxis

        if temp is None:
            return None

        return temp

    @property
    def attitude_angle(self) -> 'float':
        """float: 'AttitudeAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AttitudeAngle

        if temp is None:
            return None

        return temp

    @property
    def attitude_force(self) -> 'float':
        """float: 'AttitudeForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AttitudeForce

        if temp is None:
            return None

        return temp

    @property
    def clipped_minimum_film_thickness_at_row_centre(self) -> 'float':
        """float: 'ClippedMinimumFilmThicknessAtRowCentre' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClippedMinimumFilmThicknessAtRowCentre

        if temp is None:
            return None

        return temp

    @property
    def coefficient_of_traction(self) -> 'float':
        """float: 'CoefficientOfTraction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfTraction

        if temp is None:
            return None

        return temp

    @property
    def eccentricity_ratio(self) -> 'float':
        """float: 'EccentricityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EccentricityRatio

        if temp is None:
            return None

        return temp

    @property
    def force_x(self) -> 'float':
        """float: 'ForceX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceX

        if temp is None:
            return None

        return temp

    @property
    def force_y(self) -> 'float':
        """float: 'ForceY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceY

        if temp is None:
            return None

        return temp

    @property
    def journal_bearing_loading_chart(self) -> 'Image':
        """Image: 'JournalBearingLoadingChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.JournalBearingLoadingChart

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def minimum_film_thickness_at_row_centre(self) -> 'float':
        """float: 'MinimumFilmThicknessAtRowCentre' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumFilmThicknessAtRowCentre

        if temp is None:
            return None

        return temp

    @property
    def non_dimensional_load(self) -> 'float':
        """float: 'NonDimensionalLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NonDimensionalLoad

        if temp is None:
            return None

        return temp

    @property
    def radial_load_per_unit_of_projected_area(self) -> 'float':
        """float: 'RadialLoadPerUnitOfProjectedArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialLoadPerUnitOfProjectedArea

        if temp is None:
            return None

        return temp

    @property
    def row(self) -> '_1645.BearingRow':
        """BearingRow: 'Row' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Row

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1645.BearingRow)(value) if value is not None else None

    @property
    def sommerfeld_number(self) -> 'float':
        """float: 'SommerfeldNumber' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SommerfeldNumber

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
