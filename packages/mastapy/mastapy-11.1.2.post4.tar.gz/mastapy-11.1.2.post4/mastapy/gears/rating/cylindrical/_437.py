"""_437.py

CylindricalMeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical import _1032, _1031
from mastapy.gears import _293
from mastapy.materials import _243
from mastapy.gears.rating.cylindrical import _431, _432, _435
from mastapy.gears.rating import _338
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshSingleFlankRating',)


class CylindricalMeshSingleFlankRating(_338.MeshSingleFlankRating):
    """CylindricalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'CylindricalMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_length_of_the_line_of_action(self) -> 'float':
        """float: 'ActiveLengthOfTheLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveLengthOfTheLineOfAction

        if temp is None:
            return None

        return temp

    @property
    def axial_contact_ratio(self) -> 'float':
        """float: 'AxialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialContactRatio

        if temp is None:
            return None

        return temp

    @property
    def axial_force(self) -> 'float':
        """float: 'AxialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialForce

        if temp is None:
            return None

        return temp

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @property
    def coefficient_of_friction_method_flash_temperature_method(self) -> '_1032.ScuffingCoefficientOfFrictionMethods':
        """ScuffingCoefficientOfFrictionMethods: 'CoefficientOfFrictionMethodFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfFrictionMethodFlashTemperatureMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1032.ScuffingCoefficientOfFrictionMethods)(value) if value is not None else None

    @property
    def contact_ratio_source(self) -> '_293.ContactRatioDataSource':
        """ContactRatioDataSource: 'ContactRatioSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioSource

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_293.ContactRatioDataSource)(value) if value is not None else None

    @property
    def duration(self) -> 'float':
        """float: 'Duration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Duration

        if temp is None:
            return None

        return temp

    @property
    def dynamic_factor(self) -> 'float':
        """float: 'DynamicFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactor

        if temp is None:
            return None

        return temp

    @property
    def effective_arithmetic_mean_roughness(self) -> 'float':
        """float: 'EffectiveArithmeticMeanRoughness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveArithmeticMeanRoughness

        if temp is None:
            return None

        return temp

    @property
    def effective_face_width(self) -> 'float':
        """float: 'EffectiveFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveFaceWidth

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
    def equivalent_misalignment(self) -> 'float':
        """float: 'EquivalentMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentMisalignment

        if temp is None:
            return None

        return temp

    @property
    def face_load_factor_contact(self) -> 'float':
        """float: 'FaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorContact

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
    def gear_ratio(self) -> 'float':
        """float: 'GearRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearRatio

        if temp is None:
            return None

        return temp

    @property
    def line_of_action_parameter_of_maximum_flash_temperature(self) -> 'float':
        """float: 'LineOfActionParameterOfMaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LineOfActionParameterOfMaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def load_case(self) -> 'str':
        """str: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCase

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_factor_of_maximum_flash_temperature(self) -> 'float':
        """float: 'LoadSharingFactorOfMaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactorOfMaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def lubricant_dynamic_viscosity_at_tooth_temperature(self) -> 'float':
        """float: 'LubricantDynamicViscosityAtToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantDynamicViscosityAtToothTemperature

        if temp is None:
            return None

        return temp

    @property
    def maximum_contact_temperature(self) -> 'float':
        """float: 'MaximumContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumContactTemperature

        if temp is None:
            return None

        return temp

    @property
    def maximum_flash_temperature(self) -> 'float':
        """float: 'MaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumFlashTemperature

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
    def mean_coefficient_of_friction_of_maximum_flash_temperature(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionOfMaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCoefficientOfFrictionOfMaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def minimum_dynamic_factor_for_wind_turbine_applications(self) -> 'float':
        """float: 'MinimumDynamicFactorForWindTurbineApplications' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumDynamicFactorForWindTurbineApplications

        if temp is None:
            return None

        return temp

    @property
    def minimum_face_load_factor_for_contact_stress(self) -> 'float':
        """float: 'MinimumFaceLoadFactorForContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumFaceLoadFactorForContactStress

        if temp is None:
            return None

        return temp

    @property
    def misalignment_source(self) -> 'str':
        """str: 'MisalignmentSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentSource

        if temp is None:
            return None

        return temp

    @property
    def nominal_axial_force(self) -> 'float':
        """float: 'NominalAxialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalAxialForce

        if temp is None:
            return None

        return temp

    @property
    def nominal_radial_load(self) -> 'float':
        """float: 'NominalRadialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalRadialLoad

        if temp is None:
            return None

        return temp

    @property
    def nominal_tangential_load(self) -> 'float':
        """float: 'NominalTangentialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalTangentialLoad

        if temp is None:
            return None

        return temp

    @property
    def nominal_transverse_load(self) -> 'float':
        """float: 'NominalTransverseLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalTransverseLoad

        if temp is None:
            return None

        return temp

    @property
    def operating_normal_pressure_angle(self) -> 'float':
        """float: 'OperatingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingNormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_roll_angle_at_highest_point_of_single_tooth_contact(self) -> 'float':
        """float: 'PinionRollAngleAtHighestPointOfSingleToothContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionRollAngleAtHighestPointOfSingleToothContact

        if temp is None:
            return None

        return temp

    @property
    def pitch_line_velocity_at_operating_pitch_diameter(self) -> 'float':
        """float: 'PitchLineVelocityAtOperatingPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchLineVelocityAtOperatingPitchDiameter

        if temp is None:
            return None

        return temp

    @property
    def radial_separating_load(self) -> 'float':
        """float: 'RadialSeparatingLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialSeparatingLoad

        if temp is None:
            return None

        return temp

    @property
    def reduced_modulus_of_elasticity(self) -> 'float':
        """float: 'ReducedModulusOfElasticity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReducedModulusOfElasticity

        if temp is None:
            return None

        return temp

    @property
    def roll_angle_of_maximum_flash_temperature(self) -> 'float':
        """float: 'RollAngleOfMaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollAngleOfMaximumFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def scuffing_temperature(self) -> 'float':
        """float: 'ScuffingTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperature

        if temp is None:
            return None

        return temp

    @property
    def signed_gear_ratio(self) -> 'float':
        """float: 'SignedGearRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SignedGearRatio

        if temp is None:
            return None

        return temp

    @property
    def slideto_roll_ratio_at_end_of_active_profile(self) -> 'float':
        """float: 'SlidetoRollRatioAtEndOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidetoRollRatioAtEndOfActiveProfile

        if temp is None:
            return None

        return temp

    @property
    def slideto_roll_ratio_at_pitch_point(self) -> 'float':
        """float: 'SlidetoRollRatioAtPitchPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidetoRollRatioAtPitchPoint

        if temp is None:
            return None

        return temp

    @property
    def slideto_roll_ratio_at_start_of_active_profile(self) -> 'float':
        """float: 'SlidetoRollRatioAtStartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidetoRollRatioAtStartOfActiveProfile

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
    def tangential_velocity_at_reference_cylinder(self) -> 'float':
        """float: 'TangentialVelocityAtReferenceCylinder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialVelocityAtReferenceCylinder

        if temp is None:
            return None

        return temp

    @property
    def transmitted_tangential_load(self) -> 'float':
        """float: 'TransmittedTangentialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmittedTangentialLoad

        if temp is None:
            return None

        return temp

    @property
    def transverse_contact_ratio(self) -> 'float':
        """float: 'TransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseContactRatio

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factor_contact(self) -> 'float':
        """float: 'TransverseLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def user_specified_coefficient_of_friction_flash_temperature_method(self) -> 'float':
        """float: 'UserSpecifiedCoefficientOfFrictionFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UserSpecifiedCoefficientOfFrictionFlashTemperatureMethod

        if temp is None:
            return None

        return temp

    @property
    def virtual_contact_ratio(self) -> 'float':
        """float: 'VirtualContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualContactRatio

        if temp is None:
            return None

        return temp

    @property
    def welding_structural_factor(self) -> 'float':
        """float: 'WeldingStructuralFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WeldingStructuralFactor

        if temp is None:
            return None

        return temp

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
    def rating_settings(self) -> '_431.CylindricalGearRatingSettings':
        """CylindricalGearRatingSettings: 'RatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing(self) -> '_1031.Scuffing':
        """Scuffing: 'Scuffing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Scuffing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sorted_scuffing_results(self) -> '_432.CylindricalGearScuffingResults':
        """CylindricalGearScuffingResults: 'SortedScuffingResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SortedScuffingResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sorted_scuffing_results_without_special_values(self) -> '_432.CylindricalGearScuffingResults':
        """CylindricalGearScuffingResults: 'SortedScuffingResultsWithoutSpecialValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SortedScuffingResultsWithoutSpecialValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_single_flank_ratings(self) -> 'List[_435.CylindricalGearSingleFlankRating]':
        """List[CylindricalGearSingleFlankRating]: 'GearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSingleFlankRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
