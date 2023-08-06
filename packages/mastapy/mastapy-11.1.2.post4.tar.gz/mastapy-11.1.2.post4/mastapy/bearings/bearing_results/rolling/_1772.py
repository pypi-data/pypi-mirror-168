"""_1772.py

LoadedElement
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import _1735, _1833, _1832
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOADED_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedElement',)


class LoadedElement(_0.APIBase):
    """LoadedElement

    This is a mastapy class.
    """

    TYPE = _LOADED_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle(self) -> 'float':
        """float: 'Angle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Angle

        if temp is None:
            return None

        return temp

    @property
    def axial_loading(self) -> 'float':
        """float: 'AxialLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoading

        if temp is None:
            return None

        return temp

    @property
    def element_id(self) -> 'str':
        """str: 'ElementId' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElementId

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress(self) -> 'float':
        """float: 'MaximumNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStress

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_inner(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessInner

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_outer(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessOuter

        if temp is None:
            return None

        return temp

    @property
    def normal_load_inner(self) -> 'float':
        """float: 'NormalLoadInner' is the original name of this property."""

        temp = self.wrapped.NormalLoadInner

        if temp is None:
            return None

        return temp

    @normal_load_inner.setter
    def normal_load_inner(self, value: 'float'):
        self.wrapped.NormalLoadInner = float(value) if value else 0.0

    @property
    def normal_load_outer(self) -> 'float':
        """float: 'NormalLoadOuter' is the original name of this property."""

        temp = self.wrapped.NormalLoadOuter

        if temp is None:
            return None

        return temp

    @normal_load_outer.setter
    def normal_load_outer(self, value: 'float'):
        self.wrapped.NormalLoadOuter = float(value) if value else 0.0

    @property
    def race_deflection_inner(self) -> 'float':
        """float: 'RaceDeflectionInner' is the original name of this property."""

        temp = self.wrapped.RaceDeflectionInner

        if temp is None:
            return None

        return temp

    @race_deflection_inner.setter
    def race_deflection_inner(self, value: 'float'):
        self.wrapped.RaceDeflectionInner = float(value) if value else 0.0

    @property
    def race_deflection_outer(self) -> 'float':
        """float: 'RaceDeflectionOuter' is the original name of this property."""

        temp = self.wrapped.RaceDeflectionOuter

        if temp is None:
            return None

        return temp

    @race_deflection_outer.setter
    def race_deflection_outer(self, value: 'float'):
        self.wrapped.RaceDeflectionOuter = float(value) if value else 0.0

    @property
    def race_deflection_total(self) -> 'float':
        """float: 'RaceDeflectionTotal' is the original name of this property."""

        temp = self.wrapped.RaceDeflectionTotal

        if temp is None:
            return None

        return temp

    @race_deflection_total.setter
    def race_deflection_total(self, value: 'float'):
        self.wrapped.RaceDeflectionTotal = float(value) if value else 0.0

    @property
    def race_separation_at_element_axial(self) -> 'float':
        """float: 'RaceSeparationAtElementAxial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RaceSeparationAtElementAxial

        if temp is None:
            return None

        return temp

    @property
    def race_separation_at_element_radial(self) -> 'float':
        """float: 'RaceSeparationAtElementRadial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RaceSeparationAtElementRadial

        if temp is None:
            return None

        return temp

    @property
    def operating_internal_clearance(self) -> '_1735.InternalClearance':
        """InternalClearance: 'OperatingInternalClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingInternalClearance

        if temp is None:
            return None

        if _1735.InternalClearance.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast operating_internal_clearance to InternalClearance. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def subsurface_shear_stress_distribution_inner(self) -> 'List[_1832.StressAtPosition]':
        """List[StressAtPosition]: 'SubsurfaceShearStressDistributionInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubsurfaceShearStressDistributionInner

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def subsurface_shear_stress_distribution_outer(self) -> 'List[_1832.StressAtPosition]':
        """List[StressAtPosition]: 'SubsurfaceShearStressDistributionOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubsurfaceShearStressDistributionOuter

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
