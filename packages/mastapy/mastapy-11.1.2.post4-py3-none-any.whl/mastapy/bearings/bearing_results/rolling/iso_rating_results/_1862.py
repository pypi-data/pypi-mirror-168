"""_1862.py

ISO2812007Results
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1864
from mastapy._internal.python_net import python_net_import

_ISO2812007_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'ISO2812007Results')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO2812007Results',)


class ISO2812007Results(_1864.ISOResults):
    """ISO2812007Results

    This is a mastapy class.
    """

    TYPE = _ISO2812007_RESULTS

    def __init__(self, instance_to_wrap: 'ISO2812007Results.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def e_limiting_value_for_dynamic_equivalent_load(self) -> 'float':
        """float: 'ELimitingValueForDynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ELimitingValueForDynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def axial_to_radial_load_ratio(self) -> 'float':
        """float: 'AxialToRadialLoadRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialToRadialLoadRatio

        if temp is None:
            return None

        return temp

    @property
    def axial_to_radial_load_ratio_exceeds_iso2812007e_limiting_value_for_dynamic_equivalent_load(self) -> 'bool':
        """bool: 'AxialToRadialLoadRatioExceedsISO2812007ELimitingValueForDynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialToRadialLoadRatioExceedsISO2812007ELimitingValueForDynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_cycles(self) -> 'float':
        """float: 'BasicRatingLifeCycles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeCycles

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_damage(self) -> 'float':
        """float: 'BasicRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_damage_rate(self) -> 'float':
        """float: 'BasicRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_reliability(self) -> 'float':
        """float: 'BasicRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_safety_factor(self) -> 'float':
        """float: 'BasicRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_time(self) -> 'float':
        """float: 'BasicRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def basic_rating_life_unreliability(self) -> 'float':
        """float: 'BasicRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def calculated_viscosity_ratio(self) -> 'float':
        """float: 'CalculatedViscosityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedViscosityRatio

        if temp is None:
            return None

        return temp

    @property
    def contamination_factor(self) -> 'float':
        """float: 'ContaminationFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContaminationFactor

        if temp is None:
            return None

        return temp

    @property
    def contamination_factor_from_calculated_viscosity_ratio(self) -> 'float':
        """float: 'ContaminationFactorFromCalculatedViscosityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContaminationFactorFromCalculatedViscosityRatio

        if temp is None:
            return None

        return temp

    @property
    def dynamic_axial_load_factor(self) -> 'float':
        """float: 'DynamicAxialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAxialLoadFactor

        if temp is None:
            return None

        return temp

    @property
    def dynamic_equivalent_load(self) -> 'float':
        """float: 'DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def dynamic_radial_load_factor(self) -> 'float':
        """float: 'DynamicRadialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicRadialLoadFactor

        if temp is None:
            return None

        return temp

    @property
    def life_modification_factor_for_systems_approach(self) -> 'float':
        """float: 'LifeModificationFactorForSystemsApproach' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeModificationFactorForSystemsApproach

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_cycles(self) -> 'float':
        """float: 'ModifiedRatingLifeCycles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeCycles

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_damage(self) -> 'float':
        """float: 'ModifiedRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeDamage

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_damage_rate(self) -> 'float':
        """float: 'ModifiedRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeDamageRate

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_reliability(self) -> 'float':
        """float: 'ModifiedRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeReliability

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_safety_factor(self) -> 'float':
        """float: 'ModifiedRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_time(self) -> 'float':
        """float: 'ModifiedRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeTime

        if temp is None:
            return None

        return temp

    @property
    def modified_rating_life_unreliability(self) -> 'float':
        """float: 'ModifiedRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedRatingLifeUnreliability

        if temp is None:
            return None

        return temp

    @property
    def reference_kinematic_viscosity(self) -> 'float':
        """float: 'ReferenceKinematicViscosity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceKinematicViscosity

        if temp is None:
            return None

        return temp

    @property
    def viscosity_ratio(self) -> 'float':
        """float: 'ViscosityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ViscosityRatio

        if temp is None:
            return None

        return temp
