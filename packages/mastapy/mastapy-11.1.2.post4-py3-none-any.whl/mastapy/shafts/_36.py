"""_36.py

ShaftSectionEndDamageResults
"""


from typing import List

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.nodal_analysis import _80
from mastapy.shafts import (
    _41, _16, _17, _28
)
from mastapy.materials import _255
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_SECTION_END_DAMAGE_RESULTS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSectionEndDamageResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSectionEndDamageResults',)


class ShaftSectionEndDamageResults(_0.APIBase):
    """ShaftSectionEndDamageResults

    This is a mastapy class.
    """

    TYPE = _SHAFT_SECTION_END_DAMAGE_RESULTS

    def __init__(self, instance_to_wrap: 'ShaftSectionEndDamageResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def displacement_angular(self) -> 'Vector3D':
        """Vector3D: 'DisplacementAngular' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementAngular

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def displacement_axial(self) -> 'float':
        """float: 'DisplacementAxial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementAxial

        if temp is None:
            return None

        return temp

    @property
    def displacement_linear(self) -> 'Vector3D':
        """Vector3D: 'DisplacementLinear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementLinear

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def displacement_radial_magnitude(self) -> 'float':
        """float: 'DisplacementRadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementRadialMagnitude

        if temp is None:
            return None

        return temp

    @property
    def displacement_radial_tilt_magnitude(self) -> 'float':
        """float: 'DisplacementRadialTiltMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementRadialTiltMagnitude

        if temp is None:
            return None

        return temp

    @property
    def displacement_twist(self) -> 'float':
        """float: 'DisplacementTwist' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementTwist

        if temp is None:
            return None

        return temp

    @property
    def equivalent_alternating_stress(self) -> 'float':
        """float: 'EquivalentAlternatingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentAlternatingStress

        if temp is None:
            return None

        return temp

    @property
    def fatigue_damage(self) -> 'float':
        """float: 'FatigueDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueDamage

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor(self) -> 'float':
        """float: 'FatigueSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_for_infinite_life(self) -> 'float':
        """float: 'FatigueSafetyFactorForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorForInfiniteLife

        if temp is None:
            return None

        return temp

    @property
    def force_angular(self) -> 'Vector3D':
        """Vector3D: 'ForceAngular' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceAngular

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def force_axial(self) -> 'float':
        """float: 'ForceAxial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceAxial

        if temp is None:
            return None

        return temp

    @property
    def force_linear(self) -> 'Vector3D':
        """Vector3D: 'ForceLinear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceLinear

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def force_radial_magnitude(self) -> 'float':
        """float: 'ForceRadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceRadialMagnitude

        if temp is None:
            return None

        return temp

    @property
    def force_torque(self) -> 'float':
        """float: 'ForceTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceTorque

        if temp is None:
            return None

        return temp

    @property
    def offset(self) -> 'float':
        """float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Offset

        if temp is None:
            return None

        return temp

    @property
    def outer_diameter_to_achieve_fatigue_safety_factor_requirement(self) -> 'float':
        """float: 'OuterDiameterToAchieveFatigueSafetyFactorRequirement' is the original name of this property."""

        temp = self.wrapped.OuterDiameterToAchieveFatigueSafetyFactorRequirement

        if temp is None:
            return None

        return temp

    @outer_diameter_to_achieve_fatigue_safety_factor_requirement.setter
    def outer_diameter_to_achieve_fatigue_safety_factor_requirement(self, value: 'float'):
        self.wrapped.OuterDiameterToAchieveFatigueSafetyFactorRequirement = float(value) if value else 0.0

    @property
    def outer_radius_to_achieve_shaft_fatigue_safety_factor_requirement(self) -> 'float':
        """float: 'OuterRadiusToAchieveShaftFatigueSafetyFactorRequirement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterRadiusToAchieveShaftFatigueSafetyFactorRequirement

        if temp is None:
            return None

        return temp

    @property
    def reliability_for_infinite_life(self) -> 'float':
        """float: 'ReliabilityForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReliabilityForInfiniteLife

        if temp is None:
            return None

        return temp

    @property
    def section_end(self) -> '_80.SectionEnd':
        """SectionEnd: 'SectionEnd' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectionEnd

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_80.SectionEnd)(value) if value is not None else None

    @property
    def shaft_reliability(self) -> 'float':
        """float: 'ShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftReliability

        if temp is None:
            return None

        return temp

    @property
    def static_safety_factor(self) -> 'float':
        """float: 'StaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def total_number_of_cycles(self) -> 'float':
        """float: 'TotalNumberOfCycles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalNumberOfCycles

        if temp is None:
            return None

        return temp

    @property
    def din743201212_component_fatigue_limit_under_reversed_stress_sigma_zd_wk_sigma_bwk_tau_twk(self) -> '_41.StressMeasurementShaftAxialBendingTorsionalComponentValues':
        """StressMeasurementShaftAxialBendingTorsionalComponentValues: 'DIN743201212ComponentFatigueLimitUnderReversedStressSigmaZdWKSigmaBWKTauTWK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DIN743201212ComponentFatigueLimitUnderReversedStressSigmaZdWKSigmaBWKTauTWK

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def din743201212_component_yield_point_sigma_zd_fk_sigma_bfk_tau_tfk(self) -> '_41.StressMeasurementShaftAxialBendingTorsionalComponentValues':
        """StressMeasurementShaftAxialBendingTorsionalComponentValues: 'DIN743201212ComponentYieldPointSigmaZdFKSigmaBFKTauTFK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DIN743201212ComponentYieldPointSigmaZdFKSigmaBFKTauTFK

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def din743201212_influence_factor_for_mean_stress_sensitivity_psi_sigma_k_psi_tau_k(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        """ShaftAxialBendingTorsionalComponentValues: 'DIN743201212InfluenceFactorForMeanStressSensitivityPsiSigmaKPsiTauK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DIN743201212InfluenceFactorForMeanStressSensitivityPsiSigmaKPsiTauK

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def fkm_guideline_6th_edition_2012_cyclic_degree_of_utilization_for_finite_life(self) -> '_17.ShaftAxialBendingXBendingYTorsionalComponentValues':
        """ShaftAxialBendingXBendingYTorsionalComponentValues: 'FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForFiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForFiniteLife

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def fkm_guideline_6th_edition_2012_cyclic_degree_of_utilization_for_infinite_life(self) -> '_17.ShaftAxialBendingXBendingYTorsionalComponentValues':
        """ShaftAxialBendingXBendingYTorsionalComponentValues: 'FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForInfiniteLife

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sn_curve(self) -> '_255.SNCurve':
        """SNCurve: 'SNCurve' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SNCurve

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sn_curve_axial(self) -> '_255.SNCurve':
        """SNCurve: 'SNCurveAxial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SNCurveAxial

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sn_curve_bending_x(self) -> '_255.SNCurve':
        """SNCurve: 'SNCurveBendingX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SNCurveBendingX

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sn_curve_bending_y(self) -> '_255.SNCurve':
        """SNCurve: 'SNCurveBendingY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SNCurveBendingY

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sn_curve_torsional(self) -> '_255.SNCurve':
        """SNCurve: 'SNCurveTorsional' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SNCurveTorsional

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stress_concentration_factors(self) -> '_16.ShaftAxialBendingTorsionalComponentValues':
        """ShaftAxialBendingTorsionalComponentValues: 'StressConcentrationFactors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactors

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def din743201212_stress_amplitude_of_component_fatigue_strength_sigma_zd_adk_sigma_badk_tau_tadk(self) -> 'List[_41.StressMeasurementShaftAxialBendingTorsionalComponentValues]':
        """List[StressMeasurementShaftAxialBendingTorsionalComponentValues]: 'DIN743201212StressAmplitudeOfComponentFatigueStrengthSigmaZdADKSigmaBADKTauTADK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DIN743201212StressAmplitudeOfComponentFatigueStrengthSigmaZdADKSigmaBADKTauTADK

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def stress_cycles(self) -> 'List[_28.ShaftPointStressCycleReporting]':
        """List[ShaftPointStressCycleReporting]: 'StressCycles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCycles

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
