"""_386.py

KlingelnbergConicalMeshSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import _359
from mastapy.gears.rating import _338
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CONICAL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergConical.KN3030', 'KlingelnbergConicalMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalMeshSingleFlankRating',)


class KlingelnbergConicalMeshSingleFlankRating(_338.MeshSingleFlankRating):
    """KlingelnbergConicalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CONICAL_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def actual_integral_temperature(self) -> 'float':
        """float: 'ActualIntegralTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActualIntegralTemperature

        if temp is None:
            return None

        return temp

    @property
    def allowable_contact_stress_number(self) -> 'float':
        """float: 'AllowableContactStressNumber' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableContactStressNumber

        if temp is None:
            return None

        return temp

    @property
    def allowable_scuffing_temperature(self) -> 'float':
        """float: 'AllowableScuffingTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableScuffingTemperature

        if temp is None:
            return None

        return temp

    @property
    def alternating_load_factor(self) -> 'float':
        """float: 'AlternatingLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AlternatingLoadFactor

        if temp is None:
            return None

        return temp

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
    def bevel_gear_factor_bending(self) -> 'float':
        """float: 'BevelGearFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearFactorBending

        if temp is None:
            return None

        return temp

    @property
    def bevel_gear_factor_pitting(self) -> 'float':
        """float: 'BevelGearFactorPitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearFactorPitting

        if temp is None:
            return None

        return temp

    @property
    def contact_ratio_factor_bending(self) -> 'float':
        """float: 'ContactRatioFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactorBending

        if temp is None:
            return None

        return temp

    @property
    def contact_ratio_factor_pitting(self) -> 'float':
        """float: 'ContactRatioFactorPitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioFactorPitting

        if temp is None:
            return None

        return temp

    @property
    def contact_stress(self) -> 'float':
        """float: 'ContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStress

        if temp is None:
            return None

        return temp

    @property
    def contact_stress_limit(self) -> 'float':
        """float: 'ContactStressLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressLimit

        if temp is None:
            return None

        return temp

    @property
    def contact_stress_safety_factor(self) -> 'float':
        """float: 'ContactStressSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def dynamic_viscosity_at_sump_temperature(self) -> 'float':
        """float: 'DynamicViscosityAtSumpTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicViscosityAtSumpTemperature

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
    def helical_load_distribution_factor_scuffing(self) -> 'float':
        """float: 'HelicalLoadDistributionFactorScuffing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelicalLoadDistributionFactorScuffing

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
    def helix_angle_factor_pitting(self) -> 'float':
        """float: 'HelixAngleFactorPitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleFactorPitting

        if temp is None:
            return None

        return temp

    @property
    def load_distribution_factor_longitudinal(self) -> 'float':
        """float: 'LoadDistributionFactorLongitudinal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactorLongitudinal

        if temp is None:
            return None

        return temp

    @property
    def lubrication_factor(self) -> 'float':
        """float: 'LubricationFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricationFactor

        if temp is None:
            return None

        return temp

    @property
    def lubrication_speed_roughness_factor_product(self) -> 'float':
        """float: 'LubricationSpeedRoughnessFactorProduct' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricationSpeedRoughnessFactorProduct

        if temp is None:
            return None

        return temp

    @property
    def material_factor(self) -> 'float':
        """float: 'MaterialFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialFactor

        if temp is None:
            return None

        return temp

    @property
    def meshing_factor(self) -> 'float':
        """float: 'MeshingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshingFactor

        if temp is None:
            return None

        return temp

    @property
    def operating_oil_temperature(self) -> 'float':
        """float: 'OperatingOilTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingOilTemperature

        if temp is None:
            return None

        return temp

    @property
    def pinion_torque_of_test_gear(self) -> 'float':
        """float: 'PinionTorqueOfTestGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionTorqueOfTestGear

        if temp is None:
            return None

        return temp

    @property
    def rated_tangential_force(self) -> 'float':
        """float: 'RatedTangentialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatedTangentialForce

        if temp is None:
            return None

        return temp

    @property
    def rating_standard_name(self) -> 'str':
        """str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingStandardName

        if temp is None:
            return None

        return temp

    @property
    def relating_factor_for_the_mass_temperature(self) -> 'float':
        """float: 'RelatingFactorForTheMassTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelatingFactorForTheMassTemperature

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
    def running_in_allowance(self) -> 'float':
        """float: 'RunningInAllowance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunningInAllowance

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_scuffing(self) -> 'float':
        """float: 'SafetyFactorForScuffing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForScuffing

        if temp is None:
            return None

        return temp

    @property
    def single_meshing_factor_pinion(self) -> 'float':
        """float: 'SingleMeshingFactorPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleMeshingFactorPinion

        if temp is None:
            return None

        return temp

    @property
    def single_meshing_factor_wheel(self) -> 'float':
        """float: 'SingleMeshingFactorWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleMeshingFactorWheel

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
    def specific_line_load(self) -> 'float':
        """float: 'SpecificLineLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLineLoad

        if temp is None:
            return None

        return temp

    @property
    def stress_correction_factor(self) -> 'float':
        """float: 'StressCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def sump_temperature(self) -> 'float':
        """float: 'SumpTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumpTemperature

        if temp is None:
            return None

        return temp

    @property
    def tangential_speed(self) -> 'float':
        """float: 'TangentialSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialSpeed

        if temp is None:
            return None

        return temp

    @property
    def tip_relief_factor(self) -> 'float':
        """float: 'TipReliefFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipReliefFactor

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
    def virtual_cylindrical_gear_set(self) -> '_359.KlingelnbergVirtualCylindricalGearSet':
        """KlingelnbergVirtualCylindricalGearSet: 'VirtualCylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
