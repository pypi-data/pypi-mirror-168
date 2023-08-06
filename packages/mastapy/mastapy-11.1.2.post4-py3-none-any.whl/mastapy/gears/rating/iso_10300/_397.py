"""_397.py

ISO10300MeshSingleFlankRatingMethodB1
"""


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import (
    _365, _351, _354, _362
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.iso_10300 import _394
from mastapy._internal.python_net import python_net_import

_ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B1 = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'ISO10300MeshSingleFlankRatingMethodB1')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO10300MeshSingleFlankRatingMethodB1',)


class ISO10300MeshSingleFlankRatingMethodB1(_394.ISO10300MeshSingleFlankRating['_362.VirtualCylindricalGearISO10300MethodB1']):
    """ISO10300MeshSingleFlankRatingMethodB1

    This is a mastapy class.
    """

    TYPE = _ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B1

    def __init__(self, instance_to_wrap: 'ISO10300MeshSingleFlankRatingMethodB1.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def area_above_the_middle_contact_line_for_bending(self) -> 'float':
        """float: 'AreaAboveTheMiddleContactLineForBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaAboveTheMiddleContactLineForBending

        if temp is None:
            return None

        return temp

    @property
    def area_above_the_middle_contact_line_for_contact(self) -> 'float':
        """float: 'AreaAboveTheMiddleContactLineForContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaAboveTheMiddleContactLineForContact

        if temp is None:
            return None

        return temp

    @property
    def area_above_the_root_contact_line_for_bending(self) -> 'float':
        """float: 'AreaAboveTheRootContactLineForBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaAboveTheRootContactLineForBending

        if temp is None:
            return None

        return temp

    @property
    def area_above_the_root_contact_line_for_contact(self) -> 'float':
        """float: 'AreaAboveTheRootContactLineForContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaAboveTheRootContactLineForContact

        if temp is None:
            return None

        return temp

    @property
    def area_above_the_tip_contact_line_for_bending(self) -> 'float':
        """float: 'AreaAboveTheTipContactLineForBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaAboveTheTipContactLineForBending

        if temp is None:
            return None

        return temp

    @property
    def area_above_the_tip_contact_line_for_contact(self) -> 'float':
        """float: 'AreaAboveTheTipContactLineForContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaAboveTheTipContactLineForContact

        if temp is None:
            return None

        return temp

    @property
    def auxiliary_value_abs(self) -> 'float':
        """float: 'AuxiliaryValueABS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryValueABS

        if temp is None:
            return None

        return temp

    @property
    def auxiliary_value_bbs(self) -> 'float':
        """float: 'AuxiliaryValueBBS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryValueBBS

        if temp is None:
            return None

        return temp

    @property
    def auxiliary_value_cbs(self) -> 'float':
        """float: 'AuxiliaryValueCBS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryValueCBS

        if temp is None:
            return None

        return temp

    @property
    def average_tooth_depth(self) -> 'float':
        """float: 'AverageToothDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageToothDepth

        if temp is None:
            return None

        return temp

    @property
    def bevel_gear_factor(self) -> 'float':
        """float: 'BevelGearFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearFactor

        if temp is None:
            return None

        return temp

    @property
    def bevel_spiral_angle_factor(self) -> 'float':
        """float: 'BevelSpiralAngleFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelSpiralAngleFactor

        if temp is None:
            return None

        return temp

    @property
    def contact_ratio_factor_for_bending_method_b1(self) -> 'float':
        """float: 'ContactRatioFactorForBendingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactorForBendingMethodB1

        if temp is None:
            return None

        return temp

    @property
    def contact_stress_method_b1(self) -> 'float':
        """float: 'ContactStressMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressMethodB1

        if temp is None:
            return None

        return temp

    @property
    def contact_stress_use_bevel_slip_factor_method_b1(self) -> 'float':
        """float: 'ContactStressUseBevelSlipFactorMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressUseBevelSlipFactorMethodB1

        if temp is None:
            return None

        return temp

    @property
    def developed_length_of_one_tooth_as_the_face_width_of_the_calculation_model(self) -> 'float':
        """float: 'DevelopedLengthOfOneToothAsTheFaceWidthOfTheCalculationModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DevelopedLengthOfOneToothAsTheFaceWidthOfTheCalculationModel

        if temp is None:
            return None

        return temp

    @property
    def hypoid_factor(self) -> 'float':
        """float: 'HypoidFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidFactor

        if temp is None:
            return None

        return temp

    @property
    def inclination_angle_of_the_sum_of_velocities_vector(self) -> 'float':
        """float: 'InclinationAngleOfTheSumOfVelocitiesVector' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InclinationAngleOfTheSumOfVelocitiesVector

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_factor_bending(self) -> 'float':
        """float: 'LoadSharingFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactorBending

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_factor_pitting(self) -> 'float':
        """float: 'LoadSharingFactorPitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactorPitting

        if temp is None:
            return None

        return temp

    @property
    def mid_zone_factor(self) -> 'float':
        """float: 'MidZoneFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MidZoneFactor

        if temp is None:
            return None

        return temp

    @property
    def nominal_normal_force_of_virtual_cylindrical_gear_at_mean_point_p(self) -> 'float':
        """float: 'NominalNormalForceOfVirtualCylindricalGearAtMeanPointP' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalNormalForceOfVirtualCylindricalGearAtMeanPointP

        if temp is None:
            return None

        return temp

    @property
    def nominal_value_of_contact_stress_method_b1(self) -> 'float':
        """float: 'NominalValueOfContactStressMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalValueOfContactStressMethodB1

        if temp is None:
            return None

        return temp

    @property
    def nominal_value_of_contact_stress_using_bevel_slip_factor_method_b1(self) -> 'float':
        """float: 'NominalValueOfContactStressUsingBevelSlipFactorMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalValueOfContactStressUsingBevelSlipFactorMethodB1

        if temp is None:
            return None

        return temp

    @property
    def part_of_the_models_face_width_covered_by_the_constance(self) -> 'float':
        """float: 'PartOfTheModelsFaceWidthCoveredByTheConstance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartOfTheModelsFaceWidthCoveredByTheConstance

        if temp is None:
            return None

        return temp

    @property
    def pinion_bevel_slip_factor(self) -> 'float':
        """float: 'PinionBevelSlipFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionBevelSlipFactor

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
    def sliding_velocity_at_mean_point_p(self) -> 'float':
        """float: 'SlidingVelocityAtMeanPointP' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtMeanPointP

        if temp is None:
            return None

        return temp

    @property
    def sliding_velocity_parallel_to_the_contact_line(self) -> 'float':
        """float: 'SlidingVelocityParallelToTheContactLine' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityParallelToTheContactLine

        if temp is None:
            return None

        return temp

    @property
    def sum_of_velocities(self) -> 'float':
        """float: 'SumOfVelocities' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfVelocities

        if temp is None:
            return None

        return temp

    @property
    def sum_of_velocities_in_lengthwise_direction(self) -> 'float':
        """float: 'SumOfVelocitiesInLengthwiseDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfVelocitiesInLengthwiseDirection

        if temp is None:
            return None

        return temp

    @property
    def sum_of_velocities_in_profile_direction(self) -> 'float':
        """float: 'SumOfVelocitiesInProfileDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfVelocitiesInProfileDirection

        if temp is None:
            return None

        return temp

    @property
    def sum_of_velocities_vertical_to_the_contact_line(self) -> 'float':
        """float: 'SumOfVelocitiesVerticalToTheContactLine' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfVelocitiesVerticalToTheContactLine

        if temp is None:
            return None

        return temp

    @property
    def the_ratio_of_maximum_load_over_the_middle_contact_line_and_total_load(self) -> 'float':
        """float: 'TheRatioOfMaximumLoadOverTheMiddleContactLineAndTotalLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TheRatioOfMaximumLoadOverTheMiddleContactLineAndTotalLoad

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factors_for_bending_method_b1(self) -> 'float':
        """float: 'TransverseLoadFactorsForBendingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorsForBendingMethodB1

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factors_for_contact_method_b1(self) -> 'float':
        """float: 'TransverseLoadFactorsForContactMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorsForContactMethodB1

        if temp is None:
            return None

        return temp

    @property
    def wheel_bevel_slip_factor(self) -> 'float':
        """float: 'WheelBevelSlipFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelBevelSlipFactor

        if temp is None:
            return None

        return temp

    @property
    def virtual_cylindrical_gear_set_method_b1(self) -> '_365.VirtualCylindricalGearSetISO10300MethodB1':
        """VirtualCylindricalGearSetISO10300MethodB1: 'VirtualCylindricalGearSetMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSetMethodB1

        if temp is None:
            return None

        if _365.VirtualCylindricalGearSetISO10300MethodB1.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast virtual_cylindrical_gear_set_method_b1 to VirtualCylindricalGearSetISO10300MethodB1. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def virtual_cylindrical_gear_set_method_b1_of_type_bevel_virtual_cylindrical_gear_set_iso10300_method_b1(self) -> '_351.BevelVirtualCylindricalGearSetISO10300MethodB1':
        """BevelVirtualCylindricalGearSetISO10300MethodB1: 'VirtualCylindricalGearSetMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSetMethodB1

        if temp is None:
            return None

        if _351.BevelVirtualCylindricalGearSetISO10300MethodB1.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast virtual_cylindrical_gear_set_method_b1 to BevelVirtualCylindricalGearSetISO10300MethodB1. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def virtual_cylindrical_gear_set_method_b1_of_type_hypoid_virtual_cylindrical_gear_set_iso10300_method_b1(self) -> '_354.HypoidVirtualCylindricalGearSetISO10300MethodB1':
        """HypoidVirtualCylindricalGearSetISO10300MethodB1: 'VirtualCylindricalGearSetMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSetMethodB1

        if temp is None:
            return None

        if _354.HypoidVirtualCylindricalGearSetISO10300MethodB1.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast virtual_cylindrical_gear_set_method_b1 to HypoidVirtualCylindricalGearSetISO10300MethodB1. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
