"""_1857.py

SKFModuleResults
"""


from typing import List

from mastapy.bearings.bearing_results.rolling.skf_module import (
    _1835, _1837, _1838, _1839,
    _1840, _1842, _1846, _1850,
    _1858, _1859
)
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SKF_MODULE_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'SKFModuleResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SKFModuleResults',)


class SKFModuleResults(_0.APIBase):
    """SKFModuleResults

    This is a mastapy class.
    """

    TYPE = _SKF_MODULE_RESULTS

    def __init__(self, instance_to_wrap: 'SKFModuleResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def adjusted_speed(self) -> '_1835.AdjustedSpeed':
        """AdjustedSpeed: 'AdjustedSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdjustedSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_loads(self) -> '_1837.BearingLoads':
        """BearingLoads: 'BearingLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingLoads

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_rating_life(self) -> '_1838.BearingRatingLife':
        """BearingRatingLife: 'BearingRatingLife' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingRatingLife

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_axial_load_carrying_capacity(self) -> '_1839.DynamicAxialLoadCarryingCapacity':
        """DynamicAxialLoadCarryingCapacity: 'DynamicAxialLoadCarryingCapacity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAxialLoadCarryingCapacity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def frequencies(self) -> '_1840.Frequencies':
        """Frequencies: 'Frequencies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Frequencies

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def friction(self) -> '_1842.Friction':
        """Friction: 'Friction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Friction

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def grease_life_and_relubrication_interval(self) -> '_1846.GreaseLifeAndRelubricationInterval':
        """GreaseLifeAndRelubricationInterval: 'GreaseLifeAndRelubricationInterval' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GreaseLifeAndRelubricationInterval

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def minimum_load(self) -> '_1850.MinimumLoad':
        """MinimumLoad: 'MinimumLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def static_safety_factors(self) -> '_1858.StaticSafetyFactors':
        """StaticSafetyFactors: 'StaticSafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticSafetyFactors

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def viscosities(self) -> '_1859.Viscosities':
        """Viscosities: 'Viscosities' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Viscosities

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
