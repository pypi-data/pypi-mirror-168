"""_1722.py

LoadedRollingBearingDutyCycle
"""


from mastapy._internal import constructor
from mastapy.utility.property import (
    _1614, _1617, _1615, _1616
)
from mastapy.bearings import _1642
from mastapy.bearings.bearing_results.rolling import _1820
from mastapy.bearings.bearing_results import _1719
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLING_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedRollingBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollingBearingDutyCycle',)


class LoadedRollingBearingDutyCycle(_1719.LoadedNonLinearBearingDutyCycleResults):
    """LoadedRollingBearingDutyCycle

    This is a mastapy class.
    """

    TYPE = _LOADED_ROLLING_BEARING_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'LoadedRollingBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ansiabma_adjusted_rating_life_damage(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_adjusted_rating_life_reliability(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_adjusted_rating_life_safety_factor(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_adjusted_rating_life_time(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_adjusted_rating_life_unreliability(self) -> 'float':
        """float: 'ANSIABMAAdjustedRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMAAdjustedRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_damage(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_reliability(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_safety_factor(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_time(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_basic_rating_life_unreliability(self) -> 'float':
        """float: 'ANSIABMABasicRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMABasicRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_dynamic_equivalent_load(self) -> 'float':
        """float: 'ANSIABMADynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMADynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_basic_rating_life_damage(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_basic_rating_life_reliability(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_basic_rating_life_safety_factor(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_basic_rating_life_time(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_basic_rating_life_unreliability(self) -> 'float':
        """float: 'ISO2812007BasicRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007BasicRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_dynamic_equivalent_load(self) -> 'float':
        """float: 'ISO2812007DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007DynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_damage(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_reliability(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_safety_factor(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_time(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def iso2812007_modified_rating_life_unreliability(self) -> 'float':
        """float: 'ISO2812007ModifiedRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007ModifiedRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def iso762006_recommended_maximum_element_normal_stress(self) -> 'float':
        """float: 'ISO762006RecommendedMaximumElementNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO762006RecommendedMaximumElementNormalStress

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_damage(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_reliability(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_safety_factor(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_time(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_basic_reference_rating_life_unreliability(self) -> 'float':
        """float: 'ISOTS162812008BasicReferenceRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008BasicReferenceRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_dynamic_equivalent_load(self) -> 'float':
        """float: 'ISOTS162812008DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008DynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_damage(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_reliability(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_safety_factor(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_time(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def isots162812008_modified_reference_rating_life_unreliability(self) -> 'float':
        """float: 'ISOTS162812008ModifiedReferenceRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def lambda_ratio_inner(self) -> 'float':
        """float: 'LambdaRatioInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LambdaRatioInner

        if temp is None:
            return None

        return temp

    @property
    def lambda_ratio_outer(self) -> 'float':
        """float: 'LambdaRatioOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LambdaRatioOuter

        if temp is None:
            return None

        return temp

    @property
    def maximum_element_normal_stress(self) -> 'float':
        """float: 'MaximumElementNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStress

        if temp is None:
            return None

        return temp

    @property
    def minimum_lambda_ratio(self) -> 'float':
        """float: 'MinimumLambdaRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLambdaRatio

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness(self) -> 'float':
        """float: 'MinimumLubricatingFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThickness

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
    def skf_bearing_rating_life_damage(self) -> 'float':
        """float: 'SKFBearingRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SKFBearingRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def skf_bearing_rating_life_reliability(self) -> 'float':
        """float: 'SKFBearingRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SKFBearingRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def skf_bearing_rating_life_time(self) -> 'float':
        """float: 'SKFBearingRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SKFBearingRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def skf_bearing_rating_life_unreliability(self) -> 'float':
        """float: 'SKFBearingRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SKFBearingRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def static_equivalent_load_capacity_ratio_limit(self) -> 'float':
        """float: 'StaticEquivalentLoadCapacityRatioLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticEquivalentLoadCapacityRatioLimit

        if temp is None:
            return None

        return temp

    @property
    def worst_ansiabma_static_safety_factor(self) -> 'float':
        """float: 'WorstANSIABMAStaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorstANSIABMAStaticSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def worst_iso762006_safety_factor_static_equivalent_load_capacity_ratio(self) -> 'float':
        """float: 'WorstISO762006SafetyFactorStaticEquivalentLoadCapacityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorstISO762006SafetyFactorStaticEquivalentLoadCapacityRatio

        if temp is None:
            return None

        return temp

    @property
    def ansiabma_dynamic_equivalent_load_summary(self) -> '_1614.DutyCyclePropertySummaryForce[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ANSIABMADynamicEquivalentLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ANSIABMADynamicEquivalentLoadSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def iso2812007_dynamic_equivalent_load_summary(self) -> '_1614.DutyCyclePropertySummaryForce[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ISO2812007DynamicEquivalentLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO2812007DynamicEquivalentLoadSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def isots162812008_dynamic_equivalent_load_summary(self) -> '_1614.DutyCyclePropertySummaryForce[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ISOTS162812008DynamicEquivalentLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOTS162812008DynamicEquivalentLoadSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def maximum_element_normal_stress_inner_summary(self) -> '_1617.DutyCyclePropertySummaryStress[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryStress[BearingLoadCaseResultsLightweight]: 'MaximumElementNormalStressInnerSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressInnerSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def maximum_element_normal_stress_outer_summary(self) -> '_1617.DutyCyclePropertySummaryStress[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryStress[BearingLoadCaseResultsLightweight]: 'MaximumElementNormalStressOuterSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressOuterSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def maximum_element_normal_stress_summary(self) -> '_1617.DutyCyclePropertySummaryStress[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryStress[BearingLoadCaseResultsLightweight]: 'MaximumElementNormalStressSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumElementNormalStressSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def maximum_static_contact_stress_duty_cycle(self) -> '_1820.MaximumStaticContactStressDutyCycle':
        """MaximumStaticContactStressDutyCycle: 'MaximumStaticContactStressDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumStaticContactStressDutyCycle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def maximum_truncation_summary(self) -> '_1615.DutyCyclePropertySummaryPercentage[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryPercentage[BearingLoadCaseResultsLightweight]: 'MaximumTruncationSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTruncationSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def misalignment_summary(self) -> '_1616.DutyCyclePropertySummarySmallAngle[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummarySmallAngle[BearingLoadCaseResultsLightweight]: 'MisalignmentSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None
