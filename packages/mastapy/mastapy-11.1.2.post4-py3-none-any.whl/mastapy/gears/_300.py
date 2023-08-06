"""_300.py

GearSetDesignGroup
"""


from typing import List

from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical import _1043, _979
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears import _309
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.rating.cylindrical import _446, _431
from mastapy.materials import _232, _243
from mastapy import _0

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_GEAR_SET_DESIGN_GROUP = python_net_import('SMT.MastaAPI.Gears', 'GearSetDesignGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetDesignGroup',)


class GearSetDesignGroup(_0.APIBase):
    """GearSetDesignGroup

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_DESIGN_GROUP

    def __init__(self, instance_to_wrap: 'GearSetDesignGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def default_cylindrical_gear_material_agma(self) -> 'str':
        """str: 'DefaultCylindricalGearMaterialAGMA' is the original name of this property."""

        temp = self.wrapped.DefaultCylindricalGearMaterialAGMA.SelectedItemName

        if temp is None:
            return None

        return temp

    @default_cylindrical_gear_material_agma.setter
    def default_cylindrical_gear_material_agma(self, value: 'str'):
        self.wrapped.DefaultCylindricalGearMaterialAGMA.SetSelectedItem(str(value) if value else '')

    @property
    def default_cylindrical_gear_material_iso(self) -> 'str':
        """str: 'DefaultCylindricalGearMaterialISO' is the original name of this property."""

        temp = self.wrapped.DefaultCylindricalGearMaterialISO.SelectedItemName

        if temp is None:
            return None

        return temp

    @default_cylindrical_gear_material_iso.setter
    def default_cylindrical_gear_material_iso(self, value: 'str'):
        self.wrapped.DefaultCylindricalGearMaterialISO.SetSelectedItem(str(value) if value else '')

    @property
    def default_rough_toleranced_metal_measurement(self) -> '_1043.TolerancedMetalMeasurements':
        """TolerancedMetalMeasurements: 'DefaultRoughTolerancedMetalMeasurement' is the original name of this property."""

        temp = self.wrapped.DefaultRoughTolerancedMetalMeasurement

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1043.TolerancedMetalMeasurements)(value) if value is not None else None

    @default_rough_toleranced_metal_measurement.setter
    def default_rough_toleranced_metal_measurement(self, value: '_1043.TolerancedMetalMeasurements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DefaultRoughTolerancedMetalMeasurement = value

    @property
    def extra_backlash_for_all_gears(self) -> 'float':
        """float: 'ExtraBacklashForAllGears' is the original name of this property."""

        temp = self.wrapped.ExtraBacklashForAllGears

        if temp is None:
            return None

        return temp

    @extra_backlash_for_all_gears.setter
    def extra_backlash_for_all_gears(self, value: 'float'):
        self.wrapped.ExtraBacklashForAllGears = float(value) if value else 0.0

    @property
    def limit_dynamic_factor_if_not_in_main_resonance_range(self) -> 'bool':
        """bool: 'LimitDynamicFactorIfNotInMainResonanceRange' is the original name of this property."""

        temp = self.wrapped.LimitDynamicFactorIfNotInMainResonanceRange

        if temp is None:
            return None

        return temp

    @limit_dynamic_factor_if_not_in_main_resonance_range.setter
    def limit_dynamic_factor_if_not_in_main_resonance_range(self, value: 'bool'):
        self.wrapped.LimitDynamicFactorIfNotInMainResonanceRange = bool(value) if value else False

    @property
    def limit_micro_geometry_factor_for_the_dynamic_load(self) -> 'bool':
        """bool: 'LimitMicroGeometryFactorForTheDynamicLoad' is the original name of this property."""

        temp = self.wrapped.LimitMicroGeometryFactorForTheDynamicLoad

        if temp is None:
            return None

        return temp

    @limit_micro_geometry_factor_for_the_dynamic_load.setter
    def limit_micro_geometry_factor_for_the_dynamic_load(self, value: 'bool'):
        self.wrapped.LimitMicroGeometryFactorForTheDynamicLoad = bool(value) if value else False

    @property
    def lubrication_detail_database(self) -> 'str':
        """str: 'LubricationDetailDatabase' is the original name of this property."""

        temp = self.wrapped.LubricationDetailDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @lubrication_detail_database.setter
    def lubrication_detail_database(self, value: 'str'):
        self.wrapped.LubricationDetailDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def maximum_hunting_tooth_factor(self) -> 'float':
        """float: 'MaximumHuntingToothFactor' is the original name of this property."""

        temp = self.wrapped.MaximumHuntingToothFactor

        if temp is None:
            return None

        return temp

    @maximum_hunting_tooth_factor.setter
    def maximum_hunting_tooth_factor(self, value: 'float'):
        self.wrapped.MaximumHuntingToothFactor = float(value) if value else 0.0

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel':
        """enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property."""

        temp = self.wrapped.MicroGeometryModelInSystemDeflection

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_factor_of_safety_for_tooth_fatigue_fracture(self) -> 'float':
        """float: 'MinimumFactorOfSafetyForToothFatigueFracture' is the original name of this property."""

        temp = self.wrapped.MinimumFactorOfSafetyForToothFatigueFracture

        if temp is None:
            return None

        return temp

    @minimum_factor_of_safety_for_tooth_fatigue_fracture.setter
    def minimum_factor_of_safety_for_tooth_fatigue_fracture(self, value: 'float'):
        self.wrapped.MinimumFactorOfSafetyForToothFatigueFracture = float(value) if value else 0.0

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'float':
        """float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumPowerForGearMeshToBeLoaded

        if temp is None:
            return None

        return temp

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'float'):
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = float(value) if value else 0.0

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'float':
        """float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumTorqueForGearMeshToBeLoaded

        if temp is None:
            return None

        return temp

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'float'):
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = float(value) if value else 0.0

    @property
    def misalignment_contact_pattern_enhancement(self) -> '_446.MisalignmentContactPatternEnhancements':
        """MisalignmentContactPatternEnhancements: 'MisalignmentContactPatternEnhancement' is the original name of this property."""

        temp = self.wrapped.MisalignmentContactPatternEnhancement

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_446.MisalignmentContactPatternEnhancements)(value) if value is not None else None

    @misalignment_contact_pattern_enhancement.setter
    def misalignment_contact_pattern_enhancement(self, value: '_446.MisalignmentContactPatternEnhancements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MisalignmentContactPatternEnhancement = value

    @property
    def relative_tolerance_for_convergence(self) -> 'float':
        """float: 'RelativeToleranceForConvergence' is the original name of this property."""

        temp = self.wrapped.RelativeToleranceForConvergence

        if temp is None:
            return None

        return temp

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'float'):
        self.wrapped.RelativeToleranceForConvergence = float(value) if value else 0.0

    @property
    def required_safety_factor_for_bending(self) -> 'float':
        """float: 'RequiredSafetyFactorForBending' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForBending

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_bending.setter
    def required_safety_factor_for_bending(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForBending = float(value) if value else 0.0

    @property
    def required_safety_factor_for_contact(self) -> 'float':
        """float: 'RequiredSafetyFactorForContact' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForContact

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_contact.setter
    def required_safety_factor_for_contact(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForContact = float(value) if value else 0.0

    @property
    def required_safety_factor_for_crack_initiation(self) -> 'float':
        """float: 'RequiredSafetyFactorForCrackInitiation' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForCrackInitiation

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_crack_initiation.setter
    def required_safety_factor_for_crack_initiation(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForCrackInitiation = float(value) if value else 0.0

    @property
    def required_safety_factor_for_micropitting(self) -> 'float':
        """float: 'RequiredSafetyFactorForMicropitting' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForMicropitting

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_micropitting.setter
    def required_safety_factor_for_micropitting(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForMicropitting = float(value) if value else 0.0

    @property
    def required_safety_factor_for_scuffing(self) -> 'float':
        """float: 'RequiredSafetyFactorForScuffing' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForScuffing

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_scuffing.setter
    def required_safety_factor_for_scuffing(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForScuffing = float(value) if value else 0.0

    @property
    def required_safety_factor_for_static_bending(self) -> 'float':
        """float: 'RequiredSafetyFactorForStaticBending' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForStaticBending

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_static_bending.setter
    def required_safety_factor_for_static_bending(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForStaticBending = float(value) if value else 0.0

    @property
    def required_safety_factor_for_static_contact(self) -> 'float':
        """float: 'RequiredSafetyFactorForStaticContact' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForStaticContact

        if temp is None:
            return None

        return temp

    @required_safety_factor_for_static_contact.setter
    def required_safety_factor_for_static_contact(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForStaticContact = float(value) if value else 0.0

    @property
    def cylindrical_gear_design_constraint_settings(self) -> '_979.CylindricalGearDesignConstraintSettings':
        """CylindricalGearDesignConstraintSettings: 'CylindricalGearDesignConstraintSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearDesignConstraintSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def general_transmission_properties(self) -> '_232.GeneralTransmissionProperties':
        """GeneralTransmissionProperties: 'GeneralTransmissionProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeneralTransmissionProperties

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lubrication_detail(self) -> '_243.LubricationDetail':
        """LubricationDetail: 'LubricationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricationDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def settings(self) -> '_431.CylindricalGearRatingSettings':
        """CylindricalGearRatingSettings: 'Settings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Settings

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
