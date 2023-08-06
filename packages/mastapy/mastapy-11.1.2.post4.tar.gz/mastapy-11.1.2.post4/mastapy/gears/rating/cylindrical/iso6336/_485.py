"""_485.py

ISO6336AbstractMeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.rating.cylindrical import _446, _437
from mastapy.gears.rating.cylindrical.iso6336 import _484
from mastapy._internal.python_net import python_net_import

_ISO6336_ABSTRACT_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336AbstractMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336AbstractMeshSingleFlankRating',)


class ISO6336AbstractMeshSingleFlankRating(_437.CylindricalMeshSingleFlankRating):
    """ISO6336AbstractMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _ISO6336_ABSTRACT_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'ISO6336AbstractMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def application_factor(self) -> 'float':
        """float: 'ApplicationFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ApplicationFactor

        if temp is None:
            return None

        return temp

    @property
    def contact_ratio_factor_contact(self) -> 'float':
        """float: 'ContactRatioFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactorContact

        if temp is None:
            return None

        return temp

    @property
    def contact_ratio_factor_for_nominal_root_root_stress(self) -> 'float':
        """float: 'ContactRatioFactorForNominalRootRootStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactorForNominalRootRootStress

        if temp is None:
            return None

        return temp

    @property
    def dynamic_factor_source(self) -> 'str':
        """str: 'DynamicFactorSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactorSource

        if temp is None:
            return None

        return temp

    @property
    def elasticity_factor(self) -> 'float':
        """float: 'ElasticityFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticityFactor

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_bending(self) -> 'float':
        """float: 'FaceLoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorBending

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_contact_source(self) -> 'str':
        """str: 'FaceLoadFactorContactSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorContactSource

        if temp is None:
            return None

        return temp

    @property
    def helix_angle_factor_bending(self) -> 'float':
        """float: 'HelixAngleFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleFactorBending

        if temp is None:
            return None

        return temp

    @property
    def helix_angle_factor_contact(self) -> 'float':
        """float: 'HelixAngleFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleFactorContact

        if temp is None:
            return None

        return temp

    @property
    def mean_coefficient_of_friction_calculated_constant_flash_temperature_method(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def misalignment_contact_pattern_enhancement(self) -> '_446.MisalignmentContactPatternEnhancements':
        """MisalignmentContactPatternEnhancements: 'MisalignmentContactPatternEnhancement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentContactPatternEnhancement

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_446.MisalignmentContactPatternEnhancements)(value) if value is not None else None

    @property
    def nominal_contact_stress(self) -> 'float':
        """float: 'NominalContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalContactStress

        if temp is None:
            return None

        return temp

    @property
    def sliding_velocity_at_end_of_active_profile(self) -> 'float':
        """float: 'SlidingVelocityAtEndOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtEndOfActiveProfile

        if temp is None:
            return None

        return temp

    @property
    def sliding_velocity_at_pitch_point(self) -> 'float':
        """float: 'SlidingVelocityAtPitchPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtPitchPoint

        if temp is None:
            return None

        return temp

    @property
    def sliding_velocity_at_start_of_active_profile(self) -> 'float':
        """float: 'SlidingVelocityAtStartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtStartOfActiveProfile

        if temp is None:
            return None

        return temp

    @property
    def sum_of_tangential_velocities_at_end_of_active_profile(self) -> 'float':
        """float: 'SumOfTangentialVelocitiesAtEndOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfTangentialVelocitiesAtEndOfActiveProfile

        if temp is None:
            return None

        return temp

    @property
    def sum_of_tangential_velocities_at_pitch_point(self) -> 'float':
        """float: 'SumOfTangentialVelocitiesAtPitchPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfTangentialVelocitiesAtPitchPoint

        if temp is None:
            return None

        return temp

    @property
    def sum_of_tangential_velocities_at_start_of_active_profile(self) -> 'float':
        """float: 'SumOfTangentialVelocitiesAtStartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfTangentialVelocitiesAtStartOfActiveProfile

        if temp is None:
            return None

        return temp

    @property
    def total_contact_ratio(self) -> 'float':
        """float: 'TotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalContactRatio

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factor_bending(self) -> 'float':
        """float: 'TransverseLoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorBending

        if temp is None:
            return None

        return temp

    @property
    def zone_factor(self) -> 'float':
        """float: 'ZoneFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZoneFactor

        if temp is None:
            return None

        return temp

    @property
    def gear_single_flank_ratings(self) -> 'List[_484.ISO6336AbstractGearSingleFlankRating]':
        """List[ISO6336AbstractGearSingleFlankRating]: 'GearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def isodin_cylindrical_gear_single_flank_ratings(self) -> 'List[_484.ISO6336AbstractGearSingleFlankRating]':
        """List[ISO6336AbstractGearSingleFlankRating]: 'ISODINCylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalGearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
