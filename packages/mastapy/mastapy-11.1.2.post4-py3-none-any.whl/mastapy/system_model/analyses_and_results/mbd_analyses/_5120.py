"""_5120.py

BearingMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy.system_model.part_model import _2191
from mastapy.system_model.analyses_and_results.static_loads import _6543
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5259
from mastapy.system_model.analyses_and_results.mbd_analyses import _5150
from mastapy._internal.python_net import python_net_import

_BEARING_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BearingMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMultibodyDynamicsAnalysis',)


class BearingMultibodyDynamicsAnalysis(_5150.ConnectorMultibodyDynamicsAnalysis):
    """BearingMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _BEARING_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'BearingMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ansiabma_adjusted_rating_life_damage_rate(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_adjusted_rating_life_damage_rate_during_analysis(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeDamageRateDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeDamageRateDuringAnalysis

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_damage_rate(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_damage_rate_during_analysis(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeDamageRateDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeDamageRateDuringAnalysis

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_static_safety_factor(self) -> 'float':
        """float: 'ANSIABMAStaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAStaticSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_static_safety_factor_at_current_time(self) -> 'float':
        """float: 'ANSIABMAStaticSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAStaticSafetyFactorAtCurrentTime

        if temp is None:
            return None

        return temp

    @property
    def force(self) -> 'Vector3D':
        """Vector3D: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Force

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

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
    def iso2812007_basic_rating_life_damage_during_analysis(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeDamageDuringAnalysis

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_basic_rating_life_damage_rate(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_damage_during_analysis(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeDamageDuringAnalysis

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_damage_rate(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def iso762006_safety_factor(self) -> 'float':
        """float: 'ISO762006SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO762006SafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def iso762006_safety_factor_at_current_time(self) -> 'float':
        """float: 'ISO762006SafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO762006SafetyFactorAtCurrentTime

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_damage_during_analysis(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeDamageDuringAnalysis

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_damage_rate(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_damage_during_analysis(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeDamageDuringAnalysis

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_damage_rate(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def maximum_element_normal_stress_inner(self) -> 'float':
        """float: 'MaximumElementNormalStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressInner

        if temp is None:
            return None

        return temp

    @property
    def maximum_element_normal_stress_inner_at_current_time(self) -> 'float':
        """float: 'MaximumElementNormalStressInnerAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressInnerAtCurrentTime

        if temp is None:
            return None

        return temp

    @property
    def maximum_element_normal_stress_outer(self) -> 'float':
        """float: 'MaximumElementNormalStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressOuter

        if temp is None:
            return None

        return temp

    @property
    def maximum_element_normal_stress_outer_at_current_time(self) -> 'float':
        """float: 'MaximumElementNormalStressOuterAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressOuterAtCurrentTime

        if temp is None:
            return None

        return temp

    @property
    def maximum_static_contact_stress_inner_safety_factor(self) -> 'float':
        """float: 'MaximumStaticContactStressInnerSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumStaticContactStressInnerSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def maximum_static_contact_stress_inner_safety_factor_at_current_time(self) -> 'float':
        """float: 'MaximumStaticContactStressInnerSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumStaticContactStressInnerSafetyFactorAtCurrentTime

        if temp is None:
            return None

        return temp

    @property
    def maximum_static_contact_stress_outer_safety_factor(self) -> 'float':
        """float: 'MaximumStaticContactStressOuterSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumStaticContactStressOuterSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def maximum_static_contact_stress_outer_safety_factor_at_current_time(self) -> 'float':
        """float: 'MaximumStaticContactStressOuterSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumStaticContactStressOuterSafetyFactorAtCurrentTime

        if temp is None:
            return None

        return temp

    @property
    def relative_acceleration(self) -> 'Vector3D':
        """Vector3D: 'RelativeAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeAcceleration

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def relative_displacement(self) -> 'Vector3D':
        """Vector3D: 'RelativeDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeDisplacement

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def relative_tilt(self) -> 'Vector3D':
        """Vector3D: 'RelativeTilt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeTilt

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def relative_velocity(self) -> 'Vector3D':
        """Vector3D: 'RelativeVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeVelocity

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def component_design(self) -> '_2191.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6543.BearingLoadCase':
        """BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def peak_dynamic_force(self) -> '_5259.DynamicForceVector3DResult':
        """DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakDynamicForce

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[BearingMultibodyDynamicsAnalysis]':
        """List[BearingMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
