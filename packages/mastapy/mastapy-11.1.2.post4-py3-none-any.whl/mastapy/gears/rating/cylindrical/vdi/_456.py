"""_456.py

VDI2737InternalGearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical.iso6336 import (
    _486, _478, _480, _482
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical.din3990 import _499
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_VDI2737_INTERNAL_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.VDI', 'VDI2737InternalGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('VDI2737InternalGearSingleFlankRating',)


class VDI2737InternalGearSingleFlankRating(_0.APIBase):
    """VDI2737InternalGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _VDI2737_INTERNAL_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'VDI2737InternalGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def one_and_a_half_times_normal_module(self) -> 'float':
        """float: 'OneAndAHalfTimesNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OneAndAHalfTimesNormalModule

        if temp is None:
            return None

        return temp

    @property
    def factor_of_loading_zone_of_tooth_contact_fatigue_fracture(self) -> 'float':
        """float: 'FactorOfLoadingZoneOfToothContactFatigueFracture' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FactorOfLoadingZoneOfToothContactFatigueFracture

        if temp is None:
            return None

        return temp

    @property
    def fatigue_fracture_safety_factor(self) -> 'float':
        """float: 'FatigueFractureSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueFractureSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def fatigue_fracture_safety_factor_with_influence_of_rim(self) -> 'float':
        """float: 'FatigueFractureSafetyFactorWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueFractureSafetyFactorWithInfluenceOfRim

        if temp is None:
            return None

        return temp

    @property
    def fatigue_strength(self) -> 'float':
        """float: 'FatigueStrength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueStrength

        if temp is None:
            return None

        return temp

    @property
    def fatigue_strength_with_influence_of_rim(self) -> 'float':
        """float: 'FatigueStrengthWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueStrengthWithInfluenceOfRim

        if temp is None:
            return None

        return temp

    @property
    def form_factor_bending(self) -> 'float':
        """float: 'FormFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormFactorBending

        if temp is None:
            return None

        return temp

    @property
    def form_factor_for_compression(self) -> 'float':
        """float: 'FormFactorForCompression' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormFactorForCompression

        if temp is None:
            return None

        return temp

    @property
    def helix_factor(self) -> 'float':
        """float: 'HelixFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixFactor

        if temp is None:
            return None

        return temp

    @property
    def level_of_force_application(self) -> 'float':
        """float: 'LevelOfForceApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LevelOfForceApplication

        if temp is None:
            return None

        return temp

    @property
    def local_stress_due_to_action_of_centrifugal_force(self) -> 'float':
        """float: 'LocalStressDueToActionOfCentrifugalForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalStressDueToActionOfCentrifugalForce

        if temp is None:
            return None

        return temp

    @property
    def local_stress_due_to_the_rim_bending_moment_outside_of_the_zone_of_tooth_contact(self) -> 'float':
        """float: 'LocalStressDueToTheRimBendingMomentOutsideOfTheZoneOfToothContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalStressDueToTheRimBendingMomentOutsideOfTheZoneOfToothContact

        if temp is None:
            return None

        return temp

    @property
    def maximum_fatigue_strength(self) -> 'float':
        """float: 'MaximumFatigueStrength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumFatigueStrength

        if temp is None:
            return None

        return temp

    @property
    def mean_stress_component_compression(self) -> 'float':
        """float: 'MeanStressComponentCompression' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanStressComponentCompression

        if temp is None:
            return None

        return temp

    @property
    def mean_stress_component_2(self) -> 'float':
        """float: 'MeanStressComponent2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanStressComponent2

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def nominal_stress_due_to_action_of_centrifugal_force(self) -> 'float':
        """float: 'NominalStressDueToActionOfCentrifugalForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalStressDueToActionOfCentrifugalForce

        if temp is None:
            return None

        return temp

    @property
    def notch_sensitivity_factor_for_fatigue_strength(self) -> 'float':
        """float: 'NotchSensitivityFactorForFatigueStrength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NotchSensitivityFactorForFatigueStrength

        if temp is None:
            return None

        return temp

    @property
    def number_of_planets(self) -> 'int':
        """int: 'NumberOfPlanets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfPlanets

        if temp is None:
            return None

        return temp

    @property
    def overlap_factor(self) -> 'float':
        """float: 'OverlapFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverlapFactor

        if temp is None:
            return None

        return temp

    @property
    def peakto_peak_amplitude_of_local_stress(self) -> 'float':
        """float: 'PeaktoPeakAmplitudeOfLocalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeaktoPeakAmplitudeOfLocalStress

        if temp is None:
            return None

        return temp

    @property
    def peakto_peak_amplitude_of_local_stress_compression(self) -> 'float':
        """float: 'PeaktoPeakAmplitudeOfLocalStressCompression' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeaktoPeakAmplitudeOfLocalStressCompression

        if temp is None:
            return None

        return temp

    @property
    def peakto_peak_amplitude_of_local_stress_stiff_rim(self) -> 'float':
        """float: 'PeaktoPeakAmplitudeOfLocalStressStiffRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeaktoPeakAmplitudeOfLocalStressStiffRim

        if temp is None:
            return None

        return temp

    @property
    def position_of_maximum_local_stress(self) -> 'float':
        """float: 'PositionOfMaximumLocalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionOfMaximumLocalStress

        if temp is None:
            return None

        return temp

    @property
    def position_of_maximum_local_stress_due_to_bending_moment(self) -> 'float':
        """float: 'PositionOfMaximumLocalStressDueToBendingMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionOfMaximumLocalStressDueToBendingMoment

        if temp is None:
            return None

        return temp

    @property
    def position_of_maximum_local_stress_due_to_tangential_force(self) -> 'float':
        """float: 'PositionOfMaximumLocalStressDueToTangentialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionOfMaximumLocalStressDueToTangentialForce

        if temp is None:
            return None

        return temp

    @property
    def radial_force_in_transverse_action(self) -> 'float':
        """float: 'RadialForceInTransverseAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialForceInTransverseAction

        if temp is None:
            return None

        return temp

    @property
    def rating_name(self) -> 'str':
        """str: 'RatingName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingName

        if temp is None:
            return None

        return temp

    @property
    def reversed_fatigue_strength_of_tooth_root(self) -> 'float':
        """float: 'ReversedFatigueStrengthOfToothRoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReversedFatigueStrengthOfToothRoot

        if temp is None:
            return None

        return temp

    @property
    def safety_against_crack_initiation(self) -> 'float':
        """float: 'SafetyAgainstCrackInitiation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyAgainstCrackInitiation

        if temp is None:
            return None

        return temp

    @property
    def safety_against_crack_initiation_with_influence_of_rim(self) -> 'float':
        """float: 'SafetyAgainstCrackInitiationWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyAgainstCrackInitiationWithInfluenceOfRim

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_against_permanent_deformation(self) -> 'float':
        """float: 'SafetyFactorAgainstPermanentDeformation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorAgainstPermanentDeformation

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_against_permanent_deformation_with_influence_of_rim(self) -> 'float':
        """float: 'SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim

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
    def stress_concentration_factor(self) -> 'float':
        """float: 'StressConcentrationFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactor

        if temp is None:
            return None

        return temp

    @property
    def stress_concentration_factor_due_to_bending_moment(self) -> 'float':
        """float: 'StressConcentrationFactorDueToBendingMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactorDueToBendingMoment

        if temp is None:
            return None

        return temp

    @property
    def stress_concentration_factor_due_to_compression_by_radial_force(self) -> 'float':
        """float: 'StressConcentrationFactorDueToCompressionByRadialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactorDueToCompressionByRadialForce

        if temp is None:
            return None

        return temp

    @property
    def stress_concentration_factor_due_to_tangential_force(self) -> 'float':
        """float: 'StressConcentrationFactorDueToTangentialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactorDueToTangentialForce

        if temp is None:
            return None

        return temp

    @property
    def stress_concentration_factor_due_to_tensile_stress_in_gear_rim(self) -> 'float':
        """float: 'StressConcentrationFactorDueToTensileStressInGearRim' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactorDueToTensileStressInGearRim

        if temp is None:
            return None

        return temp

    @property
    def tangential_force_in_transverse_action(self) -> 'float':
        """float: 'TangentialForceInTransverseAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialForceInTransverseAction

        if temp is None:
            return None

        return temp

    @property
    def tensile_yield_strength_exceeded(self) -> 'bool':
        """bool: 'TensileYieldStrengthExceeded' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TensileYieldStrengthExceeded

        if temp is None:
            return None

        return temp

    @property
    def tip_factor(self) -> 'float':
        """float: 'TipFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipFactor

        if temp is None:
            return None

        return temp

    @property
    def iso_gear_rating(self) -> '_486.ISO6336AbstractMetalGearSingleFlankRating':
        """ISO6336AbstractMetalGearSingleFlankRating: 'ISOGearRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOGearRating

        if temp is None:
            return None

        if _486.ISO6336AbstractMetalGearSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso_gear_rating to ISO6336AbstractMetalGearSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso_gear_rating_of_type_iso63361996_gear_single_flank_rating(self) -> '_478.ISO63361996GearSingleFlankRating':
        """ISO63361996GearSingleFlankRating: 'ISOGearRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOGearRating

        if temp is None:
            return None

        if _478.ISO63361996GearSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso_gear_rating to ISO63361996GearSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso_gear_rating_of_type_iso63362006_gear_single_flank_rating(self) -> '_480.ISO63362006GearSingleFlankRating':
        """ISO63362006GearSingleFlankRating: 'ISOGearRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOGearRating

        if temp is None:
            return None

        if _480.ISO63362006GearSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso_gear_rating to ISO63362006GearSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso_gear_rating_of_type_iso63362019_gear_single_flank_rating(self) -> '_482.ISO63362019GearSingleFlankRating':
        """ISO63362019GearSingleFlankRating: 'ISOGearRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOGearRating

        if temp is None:
            return None

        if _482.ISO63362019GearSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso_gear_rating to ISO63362019GearSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso_gear_rating_of_type_din3990_gear_single_flank_rating(self) -> '_499.DIN3990GearSingleFlankRating':
        """DIN3990GearSingleFlankRating: 'ISOGearRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOGearRating

        if temp is None:
            return None

        if _499.DIN3990GearSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso_gear_rating to DIN3990GearSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
