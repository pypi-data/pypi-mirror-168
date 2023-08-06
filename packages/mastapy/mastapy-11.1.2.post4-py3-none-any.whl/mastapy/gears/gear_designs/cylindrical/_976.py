"""_976.py

CylindricalGearDesignConstraint
"""


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.model_validation import _1574
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.utility import _1392
from mastapy.math_utility import _1295
from mastapy.math_utility.measured_ranges import _1372
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINT = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraint')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraint',)


class CylindricalGearDesignConstraint(_0.APIBase):
    """CylindricalGearDesignConstraint

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINT

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def class_of_error(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity':
        """enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity: 'ClassOfError' is the original name of this property."""

        temp = self.wrapped.ClassOfError

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @class_of_error.setter
    def class_of_error(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ClassOfError = value

    @property
    def integer_range(self) -> '_1392.IntegerRange':
        """IntegerRange: 'IntegerRange' is the original name of this property."""

        temp = self.wrapped.IntegerRange

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @integer_range.setter
    def integer_range(self, value: '_1392.IntegerRange'):
        value = value.wrapped if value else None
        self.wrapped.IntegerRange = value

    @property
    def is_active(self) -> 'bool':
        """bool: 'IsActive' is the original name of this property."""

        temp = self.wrapped.IsActive

        if temp is None:
            return None

        return temp

    @is_active.setter
    def is_active(self, value: 'bool'):
        self.wrapped.IsActive = bool(value) if value else False

    @property
    def property_(self) -> 'str':
        """str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Property

        if temp is None:
            return None

        return temp

    @property
    def range(self) -> '_1295.Range':
        """Range: 'Range' is the original name of this property."""

        temp = self.wrapped.Range

        if temp is None:
            return None

        if _1295.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @range.setter
    def range(self, value: '_1295.Range'):
        value = value.wrapped if value else None
        self.wrapped.Range = value

    @property
    def unit(self) -> 'str':
        """str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Unit

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

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()

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
