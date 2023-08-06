"""_486.py

ISO6336AbstractMetalGearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical.iso6336 import _484
from mastapy._internal.python_net import python_net_import

_ISO6336_ABSTRACT_METAL_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336AbstractMetalGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336AbstractMetalGearSingleFlankRating',)


class ISO6336AbstractMetalGearSingleFlankRating(_484.ISO6336AbstractGearSingleFlankRating):
    """ISO6336AbstractMetalGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _ISO6336_ABSTRACT_METAL_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'ISO6336AbstractMetalGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum_contact_ratio(self) -> 'float':
        """float: 'AddendumContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AddendumContactRatio

        if temp is None:
            return None

        return temp

    @property
    def base_pitch_deviation(self) -> 'float':
        """float: 'BasePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasePitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def life_factor_for_bending_stress(self) -> 'float':
        """float: 'LifeFactorForBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorForBendingStress

        if temp is None:
            return None

        return temp

    @property
    def life_factor_for_contact_stress(self) -> 'float':
        """float: 'LifeFactorForContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorForContactStress

        if temp is None:
            return None

        return temp

    @property
    def life_factor_for_reference_bending_stress(self) -> 'float':
        """float: 'LifeFactorForReferenceBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorForReferenceBendingStress

        if temp is None:
            return None

        return temp

    @property
    def life_factor_for_reference_contact_stress(self) -> 'float':
        """float: 'LifeFactorForReferenceContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorForReferenceContactStress

        if temp is None:
            return None

        return temp

    @property
    def life_factor_for_static_bending_stress(self) -> 'float':
        """float: 'LifeFactorForStaticBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorForStaticBendingStress

        if temp is None:
            return None

        return temp

    @property
    def life_factor_for_static_contact_stress(self) -> 'float':
        """float: 'LifeFactorForStaticContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorForStaticContactStress

        if temp is None:
            return None

        return temp

    @property
    def lubricant_factor(self) -> 'float':
        """float: 'LubricantFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantFactor

        if temp is None:
            return None

        return temp

    @property
    def lubricant_factor_for_reference_stress(self) -> 'float':
        """float: 'LubricantFactorForReferenceStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantFactorForReferenceStress

        if temp is None:
            return None

        return temp

    @property
    def lubricant_factor_for_static_stress(self) -> 'float':
        """float: 'LubricantFactorForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantFactorForStaticStress

        if temp is None:
            return None

        return temp

    @property
    def moment_of_inertia_per_unit_face_width(self) -> 'float':
        """float: 'MomentOfInertiaPerUnitFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MomentOfInertiaPerUnitFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def profile_form_deviation(self) -> 'float':
        """float: 'ProfileFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileFormDeviation

        if temp is None:
            return None

        return temp

    @property
    def relative_individual_gear_mass_per_unit_face_width_referenced_to_line_of_action(self) -> 'float':
        """float: 'RelativeIndividualGearMassPerUnitFaceWidthReferencedToLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeIndividualGearMassPerUnitFaceWidthReferencedToLineOfAction

        if temp is None:
            return None

        return temp

    @property
    def relative_notch_sensitivity_factor(self) -> 'float':
        """float: 'RelativeNotchSensitivityFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeNotchSensitivityFactor

        if temp is None:
            return None

        return temp

    @property
    def relative_notch_sensitivity_factor_for_reference_stress(self) -> 'float':
        """float: 'RelativeNotchSensitivityFactorForReferenceStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeNotchSensitivityFactorForReferenceStress

        if temp is None:
            return None

        return temp

    @property
    def relative_notch_sensitivity_factor_for_static_stress(self) -> 'float':
        """float: 'RelativeNotchSensitivityFactorForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeNotchSensitivityFactorForStaticStress

        if temp is None:
            return None

        return temp

    @property
    def relative_surface_factor(self) -> 'float':
        """float: 'RelativeSurfaceFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeSurfaceFactor

        if temp is None:
            return None

        return temp

    @property
    def relative_surface_factor_for_reference_stress(self) -> 'float':
        """float: 'RelativeSurfaceFactorForReferenceStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeSurfaceFactorForReferenceStress

        if temp is None:
            return None

        return temp

    @property
    def relative_surface_factor_for_static_stress(self) -> 'float':
        """float: 'RelativeSurfaceFactorForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeSurfaceFactorForStaticStress

        if temp is None:
            return None

        return temp

    @property
    def roughness_factor(self) -> 'float':
        """float: 'RoughnessFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughnessFactor

        if temp is None:
            return None

        return temp

    @property
    def roughness_factor_for_reference_stress(self) -> 'float':
        """float: 'RoughnessFactorForReferenceStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughnessFactorForReferenceStress

        if temp is None:
            return None

        return temp

    @property
    def roughness_factor_for_static_stress(self) -> 'float':
        """float: 'RoughnessFactorForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughnessFactorForStaticStress

        if temp is None:
            return None

        return temp

    @property
    def shot_peening_bending_stress_benefit(self) -> 'float':
        """float: 'ShotPeeningBendingStressBenefit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShotPeeningBendingStressBenefit

        if temp is None:
            return None

        return temp

    @property
    def single_pair_tooth_contact_factor(self) -> 'float':
        """float: 'SinglePairToothContactFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SinglePairToothContactFactor

        if temp is None:
            return None

        return temp

    @property
    def size_factor(self) -> 'float':
        """float: 'SizeFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactor

        if temp is None:
            return None

        return temp

    @property
    def size_factor_tooth_root(self) -> 'float':
        """float: 'SizeFactorToothRoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorToothRoot

        if temp is None:
            return None

        return temp

    @property
    def size_factor_for_reference_bending_stress(self) -> 'float':
        """float: 'SizeFactorForReferenceBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorForReferenceBendingStress

        if temp is None:
            return None

        return temp

    @property
    def size_factor_for_reference_contact_stress(self) -> 'float':
        """float: 'SizeFactorForReferenceContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorForReferenceContactStress

        if temp is None:
            return None

        return temp

    @property
    def size_factor_for_static_stress(self) -> 'float':
        """float: 'SizeFactorForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorForStaticStress

        if temp is None:
            return None

        return temp

    @property
    def static_size_factor_tooth_root(self) -> 'float':
        """float: 'StaticSizeFactorToothRoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticSizeFactorToothRoot

        if temp is None:
            return None

        return temp

    @property
    def velocity_factor(self) -> 'float':
        """float: 'VelocityFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VelocityFactor

        if temp is None:
            return None

        return temp

    @property
    def velocity_factor_for_reference_stress(self) -> 'float':
        """float: 'VelocityFactorForReferenceStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VelocityFactorForReferenceStress

        if temp is None:
            return None

        return temp

    @property
    def velocity_factor_for_static_stress(self) -> 'float':
        """float: 'VelocityFactorForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VelocityFactorForStaticStress

        if temp is None:
            return None

        return temp

    @property
    def work_hardening_factor(self) -> 'float':
        """float: 'WorkHardeningFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkHardeningFactor

        if temp is None:
            return None

        return temp
