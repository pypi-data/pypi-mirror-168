"""_196.py

MaterialPropertiesReporting
"""


from typing import List

from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.fe_tools.enums import _1194
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
    _185, _198, _200, _201
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MATERIAL_PROPERTIES_REPORTING = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'MaterialPropertiesReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialPropertiesReporting',)


class MaterialPropertiesReporting(_0.APIBase):
    """MaterialPropertiesReporting

    This is a mastapy class.
    """

    TYPE = _MATERIAL_PROPERTIES_REPORTING

    def __init__(self, instance_to_wrap: 'MaterialPropertiesReporting.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def class_(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass':
        """enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass: 'Class' is the original name of this property."""

        temp = self.wrapped.Class

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @class_.setter
    def class_(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MaterialPropertyClass.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Class = value

    @property
    def density(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Density' is the original name of this property."""

        temp = self.wrapped.Density

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @density.setter
    def density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Density = value

    @property
    def elastic_stiffness_tensor_lower_triangle(self) -> 'str':
        """str: 'ElasticStiffnessTensorLowerTriangle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticStiffnessTensorLowerTriangle

        if temp is None:
            return None

        return temp

    @property
    def id(self) -> 'int':
        """int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ID

        if temp is None:
            return None

        return temp

    @property
    def modulus_of_elasticity(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ModulusOfElasticity' is the original name of this property."""

        temp = self.wrapped.ModulusOfElasticity

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @modulus_of_elasticity.setter
    def modulus_of_elasticity(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ModulusOfElasticity = value

    @property
    def poissons_ratio(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PoissonsRatio' is the original name of this property."""

        temp = self.wrapped.PoissonsRatio

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @poissons_ratio.setter
    def poissons_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PoissonsRatio = value

    @property
    def thermal_expansion_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ThermalExpansionCoefficient' is the original name of this property."""

        temp = self.wrapped.ThermalExpansionCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @thermal_expansion_coefficient.setter
    def thermal_expansion_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ThermalExpansionCoefficient = value

    @property
    def elastic_modulus_components(self) -> '_185.ElasticModulusOrthotropicComponents':
        """ElasticModulusOrthotropicComponents: 'ElasticModulusComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticModulusComponents

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def poissons_ratio_components(self) -> '_198.PoissonRatioOrthotropicComponents':
        """PoissonRatioOrthotropicComponents: 'PoissonsRatioComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PoissonsRatioComponents

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shear_modulus_components(self) -> '_200.ShearModulusOrthotropicComponents':
        """ShearModulusOrthotropicComponents: 'ShearModulusComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearModulusComponents

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def thermal_expansion_coefficient_components(self) -> '_201.ThermalExpansionOrthotropicComponents':
        """ThermalExpansionOrthotropicComponents: 'ThermalExpansionCoefficientComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermalExpansionCoefficientComponents

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
