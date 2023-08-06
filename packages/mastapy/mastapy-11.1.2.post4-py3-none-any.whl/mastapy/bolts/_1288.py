"""_1288.py

LoadedBolt
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bolts import (
    _1271, _1287, _1293, _1283
)
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOADED_BOLT = python_net_import('SMT.MastaAPI.Bolts', 'LoadedBolt')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBolt',)


class LoadedBolt(_0.APIBase):
    """LoadedBolt

    This is a mastapy class.
    """

    TYPE = _LOADED_BOLT

    def __init__(self, instance_to_wrap: 'LoadedBolt.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def additional_axial_bolt_load(self) -> 'float':
        """float: 'AdditionalAxialBoltLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalAxialBoltLoad

        if temp is None:
            return None

        return temp

    @property
    def additional_axial_bolt_load_in_assembled_state(self) -> 'float':
        """float: 'AdditionalAxialBoltLoadInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalAxialBoltLoadInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def additional_bending_moment(self) -> 'float':
        """float: 'AdditionalBendingMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalBendingMoment

        if temp is None:
            return None

        return temp

    @property
    def additional_bending_moment_in_bolt(self) -> 'float':
        """float: 'AdditionalBendingMomentInBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalBendingMomentInBolt

        if temp is None:
            return None

        return temp

    @property
    def additional_bolt_load_after_opening(self) -> 'float':
        """float: 'AdditionalBoltLoadAfterOpening' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalBoltLoadAfterOpening

        if temp is None:
            return None

        return temp

    @property
    def alternating_stress(self) -> 'float':
        """float: 'AlternatingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AlternatingStress

        if temp is None:
            return None

        return temp

    @property
    def alternating_stress_eccentric(self) -> 'float':
        """float: 'AlternatingStressEccentric' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AlternatingStressEccentric

        if temp is None:
            return None

        return temp

    @property
    def assembly_preload(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AssemblyPreload' is the original name of this property."""

        temp = self.wrapped.AssemblyPreload

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @assembly_preload.setter
    def assembly_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AssemblyPreload = value

    @property
    def assembly_temperature(self) -> 'float':
        """float: 'AssemblyTemperature' is the original name of this property."""

        temp = self.wrapped.AssemblyTemperature

        if temp is None:
            return None

        return temp

    @assembly_temperature.setter
    def assembly_temperature(self, value: 'float'):
        self.wrapped.AssemblyTemperature = float(value) if value else 0.0

    @property
    def average_bolt_load(self) -> 'float':
        """float: 'AverageBoltLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageBoltLoad

        if temp is None:
            return None

        return temp

    @property
    def average_bolt_load_maximum_assembly_preload(self) -> 'float':
        """float: 'AverageBoltLoadMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageBoltLoadMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def average_bolt_load_minimum_assembly_preload(self) -> 'float':
        """float: 'AverageBoltLoadMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageBoltLoadMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def axial_load_type(self) -> '_1271.AxialLoadType':
        """AxialLoadType: 'AxialLoadType' is the original name of this property."""

        temp = self.wrapped.AxialLoadType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1271.AxialLoadType)(value) if value is not None else None

    @axial_load_type.setter
    def axial_load_type(self, value: '_1271.AxialLoadType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AxialLoadType = value

    @property
    def axial_load_at_opening_limit_concentric_loading(self) -> 'float':
        """float: 'AxialLoadAtOpeningLimitConcentricLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoadAtOpeningLimitConcentricLoading

        if temp is None:
            return None

        return temp

    @property
    def axial_load_at_opening_limit_eccentric_loading(self) -> 'float':
        """float: 'AxialLoadAtOpeningLimitEccentricLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoadAtOpeningLimitEccentricLoading

        if temp is None:
            return None

        return temp

    @property
    def axial_load_at_opening_limit_eccentric_loading_from_5329(self) -> 'float':
        """float: 'AxialLoadAtOpeningLimitEccentricLoadingFrom5329' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoadAtOpeningLimitEccentricLoadingFrom5329

        if temp is None:
            return None

        return temp

    @property
    def axial_load_at_which_opening_occurs_during_eccentric_loading(self) -> 'float':
        """float: 'AxialLoadAtWhichOpeningOccursDuringEccentricLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoadAtWhichOpeningOccursDuringEccentricLoading

        if temp is None:
            return None

        return temp

    @property
    def bending_angle(self) -> 'float':
        """float: 'BendingAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingAngle

        if temp is None:
            return None

        return temp

    @property
    def bending_moment(self) -> 'float':
        """float: 'BendingMoment' is the original name of this property."""

        temp = self.wrapped.BendingMoment

        if temp is None:
            return None

        return temp

    @bending_moment.setter
    def bending_moment(self, value: 'float'):
        self.wrapped.BendingMoment = float(value) if value else 0.0

    @property
    def bending_moment_at_bolting_point(self) -> 'float':
        """float: 'BendingMomentAtBoltingPoint' is the original name of this property."""

        temp = self.wrapped.BendingMomentAtBoltingPoint

        if temp is None:
            return None

        return temp

    @bending_moment_at_bolting_point.setter
    def bending_moment_at_bolting_point(self, value: 'float'):
        self.wrapped.BendingMomentAtBoltingPoint = float(value) if value else 0.0

    @property
    def breaking_force(self) -> 'float':
        """float: 'BreakingForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BreakingForce

        if temp is None:
            return None

        return temp

    @property
    def change_in_preload_due_to_thermal_expansion(self) -> 'float':
        """float: 'ChangeInPreloadDueToThermalExpansion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChangeInPreloadDueToThermalExpansion

        if temp is None:
            return None

        return temp

    @property
    def change_in_temperature_of_bolt(self) -> 'float':
        """float: 'ChangeInTemperatureOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChangeInTemperatureOfBolt

        if temp is None:
            return None

        return temp

    @property
    def change_in_temperature_of_clamped_parts(self) -> 'float':
        """float: 'ChangeInTemperatureOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChangeInTemperatureOfClampedParts

        if temp is None:
            return None

        return temp

    @property
    def clamp_load_at_opening_limit(self) -> 'float':
        """float: 'ClampLoadAtOpeningLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClampLoadAtOpeningLimit

        if temp is None:
            return None

        return temp

    @property
    def clamping_load(self) -> 'float':
        """float: 'ClampingLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClampingLoad

        if temp is None:
            return None

        return temp

    @property
    def comparative_stress_in_assembled_state(self) -> 'float':
        """float: 'ComparativeStressInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComparativeStressInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def comparative_stress_in_assembled_state_maximum_assembly_preload(self) -> 'float':
        """float: 'ComparativeStressInAssembledStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComparativeStressInAssembledStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def comparative_stress_in_working_state(self) -> 'float':
        """float: 'ComparativeStressInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComparativeStressInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def comparative_stress_in_working_state_maximum_assembly_preload(self) -> 'float':
        """float: 'ComparativeStressInWorkingStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComparativeStressInWorkingStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def comparative_stress_in_working_state_minimum_assembly_preload(self) -> 'float':
        """float: 'ComparativeStressInWorkingStateMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComparativeStressInWorkingStateMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def correction_factor_c1(self) -> 'float':
        """float: 'CorrectionFactorC1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CorrectionFactorC1

        if temp is None:
            return None

        return temp

    @property
    def correction_factor_c3(self) -> 'float':
        """float: 'CorrectionFactorC3' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CorrectionFactorC3

        if temp is None:
            return None

        return temp

    @property
    def distance_between_edge_of_preloading_area_and_force_introduction_point(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DistanceBetweenEdgeOfPreloadingAreaAndForceIntroductionPoint' is the original name of this property."""

        temp = self.wrapped.DistanceBetweenEdgeOfPreloadingAreaAndForceIntroductionPoint

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @distance_between_edge_of_preloading_area_and_force_introduction_point.setter
    def distance_between_edge_of_preloading_area_and_force_introduction_point(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DistanceBetweenEdgeOfPreloadingAreaAndForceIntroductionPoint = value

    @property
    def distance_of_edge_bearing_point_v_from_centre(self) -> 'float':
        """float: 'DistanceOfEdgeBearingPointVFromCentre' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DistanceOfEdgeBearingPointVFromCentre

        if temp is None:
            return None

        return temp

    @property
    def distance_of_line_of_action_of_axial_load_from_centre(self) -> 'float':
        """float: 'DistanceOfLineOfActionOfAxialLoadFromCentre' is the original name of this property."""

        temp = self.wrapped.DistanceOfLineOfActionOfAxialLoadFromCentre

        if temp is None:
            return None

        return temp

    @distance_of_line_of_action_of_axial_load_from_centre.setter
    def distance_of_line_of_action_of_axial_load_from_centre(self, value: 'float'):
        self.wrapped.DistanceOfLineOfActionOfAxialLoadFromCentre = float(value) if value else 0.0

    @property
    def does_tightening_technique_exceed_yield_point(self) -> 'bool':
        """bool: 'DoesTighteningTechniqueExceedYieldPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DoesTighteningTechniqueExceedYieldPoint

        if temp is None:
            return None

        return temp

    @property
    def edge_distance_of_opening_point_u(self) -> 'float':
        """float: 'EdgeDistanceOfOpeningPointU' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EdgeDistanceOfOpeningPointU

        if temp is None:
            return None

        return temp

    @property
    def effective_diameter_of_friction_moment(self) -> 'float':
        """float: 'EffectiveDiameterOfFrictionMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveDiameterOfFrictionMoment

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_bolt(self) -> 'float':
        """float: 'ElasticResilienceOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfBolt

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_bolt_at_room_temperature(self) -> 'float':
        """float: 'ElasticResilienceOfBoltAtRoomTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfBoltAtRoomTemperature

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_bolt_in_operating_state(self) -> 'float':
        """float: 'ElasticResilienceOfBoltInOperatingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfBoltInOperatingState

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_plates_at_room_temperature(self) -> 'float':
        """float: 'ElasticResilienceOfPlatesAtRoomTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfPlatesAtRoomTemperature

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_maximum_required_assembly_preload(self) -> 'float':
        """float: 'FatigueSafetyFactorMaximumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorMaximumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_minimum_required_assembly_preload(self) -> 'float':
        """float: 'FatigueSafetyFactorMinimumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorMinimumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_in_assembled_state(self) -> 'float':
        """float: 'FatigueSafetyFactorInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_in_working_state(self) -> 'float':
        """float: 'FatigueSafetyFactorInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_in_the_assembled_state_maximum_required_assembly_preload(self) -> 'float':
        """float: 'FatigueSafetyFactorInTheAssembledStateMaximumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorInTheAssembledStateMaximumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def fatigue_safety_factor_in_the_assembled_state_minimum_required_assembly_preload(self) -> 'float':
        """float: 'FatigueSafetyFactorInTheAssembledStateMinimumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueSafetyFactorInTheAssembledStateMinimumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def joint_type(self) -> '_1287.JointTypes':
        """JointTypes: 'JointType' is the original name of this property."""

        temp = self.wrapped.JointType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1287.JointTypes)(value) if value is not None else None

    @joint_type.setter
    def joint_type(self, value: '_1287.JointTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.JointType = value

    @property
    def joint_is_to_be_designed_with_f_qmax(self) -> 'bool':
        """bool: 'JointIsToBeDesignedWithFQmax' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.JointIsToBeDesignedWithFQmax

        if temp is None:
            return None

        return temp

    @property
    def length_between_basic_solid_and_load_introduction_point_k(self) -> 'float':
        """float: 'LengthBetweenBasicSolidAndLoadIntroductionPointK' is the original name of this property."""

        temp = self.wrapped.LengthBetweenBasicSolidAndLoadIntroductionPointK

        if temp is None:
            return None

        return temp

    @length_between_basic_solid_and_load_introduction_point_k.setter
    def length_between_basic_solid_and_load_introduction_point_k(self, value: 'float'):
        self.wrapped.LengthBetweenBasicSolidAndLoadIntroductionPointK = float(value) if value else 0.0

    @property
    def limiting_slip_force(self) -> 'float':
        """float: 'LimitingSlipForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingSlipForce

        if temp is None:
            return None

        return temp

    @property
    def limiting_surface_pressure_on_head_side(self) -> 'float':
        """float: 'LimitingSurfacePressureOnHeadSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingSurfacePressureOnHeadSide

        if temp is None:
            return None

        return temp

    @property
    def limiting_surface_pressure_on_nut_side(self) -> 'float':
        """float: 'LimitingSurfacePressureOnNutSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingSurfacePressureOnNutSide

        if temp is None:
            return None

        return temp

    @property
    def load_factor(self) -> 'float':
        """float: 'LoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactor

        if temp is None:
            return None

        return temp

    @property
    def load_factor_bending(self) -> 'float':
        """float: 'LoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorBending

        if temp is None:
            return None

        return temp

    @property
    def load_factor_phi_stare_k(self) -> 'float':
        """float: 'LoadFactorPhiStareK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorPhiStareK

        if temp is None:
            return None

        return temp

    @property
    def load_factor_for_concentric_clamping(self) -> 'float':
        """float: 'LoadFactorForConcentricClamping' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorForConcentricClamping

        if temp is None:
            return None

        return temp

    @property
    def load_factor_for_concentric_clamping_in_operating_state(self) -> 'float':
        """float: 'LoadFactorForConcentricClampingInOperatingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorForConcentricClampingInOperatingState

        if temp is None:
            return None

        return temp

    @property
    def load_factor_for_eccentric_clamping(self) -> 'float':
        """float: 'LoadFactorForEccentricClamping' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorForEccentricClamping

        if temp is None:
            return None

        return temp

    @property
    def load_factor_for_eccentric_clamping_and_concentric_load_introduction(self) -> 'float':
        """float: 'LoadFactorForEccentricClampingAndConcentricLoadIntroduction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadFactorForEccentricClampingAndConcentricLoadIntroduction

        if temp is None:
            return None

        return temp

    @property
    def load_introduction_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LoadIntroductionFactor' is the original name of this property."""

        temp = self.wrapped.LoadIntroductionFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @load_introduction_factor.setter
    def load_introduction_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LoadIntroductionFactor = value

    @property
    def load_at_minimum_yield_point(self) -> 'float':
        """float: 'LoadAtMinimumYieldPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadAtMinimumYieldPoint

        if temp is None:
            return None

        return temp

    @property
    def loss_of_preload_due_to_embedding(self) -> 'float':
        """float: 'LossOfPreloadDueToEmbedding' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LossOfPreloadDueToEmbedding

        if temp is None:
            return None

        return temp

    @property
    def maximum_additional_axial_load(self) -> 'float':
        """float: 'MaximumAdditionalAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAdditionalAxialLoad

        if temp is None:
            return None

        return temp

    @property
    def maximum_assembly_preload(self) -> 'float':
        """float: 'MaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_assembly_preload_during_assembly(self) -> 'float':
        """float: 'MaximumAssemblyPreloadDuringAssembly' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAssemblyPreloadDuringAssembly

        if temp is None:
            return None

        return temp

    @property
    def maximum_axial_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaximumAxialLoad' is the original name of this property."""

        temp = self.wrapped.MaximumAxialLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @maximum_axial_load.setter
    def maximum_axial_load(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaximumAxialLoad = value

    @property
    def maximum_head_surface_pressure_in_assembled_state(self) -> 'float':
        """float: 'MaximumHeadSurfacePressureInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumHeadSurfacePressureInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def maximum_head_surface_pressure_in_working_state(self) -> 'float':
        """float: 'MaximumHeadSurfacePressureInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumHeadSurfacePressureInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def maximum_nut_surface_pressure_in_assembled_state(self) -> 'float':
        """float: 'MaximumNutSurfacePressureInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNutSurfacePressureInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def maximum_nut_surface_pressure_in_working_state(self) -> 'float':
        """float: 'MaximumNutSurfacePressureInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNutSurfacePressureInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def maximum_preload(self) -> 'float':
        """float: 'MaximumPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_preload_maximum_assembly_preload(self) -> 'float':
        """float: 'MaximumPreloadMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumPreloadMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_preload_minimum_assembly_preload(self) -> 'float':
        """float: 'MaximumPreloadMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumPreloadMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_preload_in_assembled_state_maximum_assembly_preload(self) -> 'float':
        """float: 'MaximumPreloadInAssembledStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumPreloadInAssembledStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_pressure_to_be_sealed(self) -> 'float':
        """float: 'MaximumPressureToBeSealed' is the original name of this property."""

        temp = self.wrapped.MaximumPressureToBeSealed

        if temp is None:
            return None

        return temp

    @maximum_pressure_to_be_sealed.setter
    def maximum_pressure_to_be_sealed(self, value: 'float'):
        self.wrapped.MaximumPressureToBeSealed = float(value) if value else 0.0

    @property
    def maximum_relieving_load_of_plates(self) -> 'float':
        """float: 'MaximumRelievingLoadOfPlates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRelievingLoadOfPlates

        if temp is None:
            return None

        return temp

    @property
    def maximum_stress_in_bending_tension_of_bolt_thread(self) -> 'float':
        """float: 'MaximumStressInBendingTensionOfBoltThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumStressInBendingTensionOfBoltThread

        if temp is None:
            return None

        return temp

    @property
    def maximum_surface_pressure(self) -> 'float':
        """float: 'MaximumSurfacePressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSurfacePressure

        if temp is None:
            return None

        return temp

    @property
    def maximum_surface_pressure_in_assembled_state(self) -> 'float':
        """float: 'MaximumSurfacePressureInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSurfacePressureInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def maximum_surface_pressure_in_assembled_state_maximum_assembly_preload(self) -> 'float':
        """float: 'MaximumSurfacePressureInAssembledStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSurfacePressureInAssembledStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_surface_pressure_in_working_state(self) -> 'float':
        """float: 'MaximumSurfacePressureInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSurfacePressureInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def maximum_surface_pressure_in_working_state_maximum_assembly_preload(self) -> 'float':
        """float: 'MaximumSurfacePressureInWorkingStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSurfacePressureInWorkingStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_surface_pressure_in_working_state_minimum_assembly_preload(self) -> 'float':
        """float: 'MaximumSurfacePressureInWorkingStateMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSurfacePressureInWorkingStateMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_tensile_stress(self) -> 'float':
        """float: 'MaximumTensileStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTensileStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_tensile_stress_in_working_state_maximum_assembly_preload(self) -> 'float':
        """float: 'MaximumTensileStressInWorkingStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTensileStressInWorkingStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_tensile_stress_in_working_state_minimum_assembly_preload(self) -> 'float':
        """float: 'MaximumTensileStressInWorkingStateMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTensileStressInWorkingStateMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def maximum_torque_about_bolt_axis(self) -> 'float':
        """float: 'MaximumTorqueAboutBoltAxis' is the original name of this property."""

        temp = self.wrapped.MaximumTorqueAboutBoltAxis

        if temp is None:
            return None

        return temp

    @maximum_torque_about_bolt_axis.setter
    def maximum_torque_about_bolt_axis(self, value: 'float'):
        self.wrapped.MaximumTorqueAboutBoltAxis = float(value) if value else 0.0

    @property
    def maximum_torsional_moment(self) -> 'float':
        """float: 'MaximumTorsionalMoment' is the original name of this property."""

        temp = self.wrapped.MaximumTorsionalMoment

        if temp is None:
            return None

        return temp

    @maximum_torsional_moment.setter
    def maximum_torsional_moment(self, value: 'float'):
        self.wrapped.MaximumTorsionalMoment = float(value) if value else 0.0

    @property
    def maximum_torsional_stress(self) -> 'float':
        """float: 'MaximumTorsionalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTorsionalStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_torsional_stress_due_to_fq(self) -> 'float':
        """float: 'MaximumTorsionalStressDueToFQ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTorsionalStressDueToFQ

        if temp is None:
            return None

        return temp

    @property
    def maximum_transverse_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaximumTransverseLoad' is the original name of this property."""

        temp = self.wrapped.MaximumTransverseLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @maximum_transverse_load.setter
    def maximum_transverse_load(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaximumTransverseLoad = value

    @property
    def minimum_additional_axial_load(self) -> 'float':
        """float: 'MinimumAdditionalAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAdditionalAxialLoad

        if temp is None:
            return None

        return temp

    @property
    def minimum_assembly_preload(self) -> 'float':
        """float: 'MinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def minimum_assembly_preload_during_assembly(self) -> 'float':
        """float: 'MinimumAssemblyPreloadDuringAssembly' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAssemblyPreloadDuringAssembly

        if temp is None:
            return None

        return temp

    @property
    def minimum_axial_load(self) -> 'float':
        """float: 'MinimumAxialLoad' is the original name of this property."""

        temp = self.wrapped.MinimumAxialLoad

        if temp is None:
            return None

        return temp

    @minimum_axial_load.setter
    def minimum_axial_load(self, value: 'float'):
        self.wrapped.MinimumAxialLoad = float(value) if value else 0.0

    @property
    def minimum_clamp_load_for_ensuring_a_sealing_function(self) -> 'float':
        """float: 'MinimumClampLoadForEnsuringASealingFunction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumClampLoadForEnsuringASealingFunction

        if temp is None:
            return None

        return temp

    @property
    def minimum_clamp_load_at_the_opening_limit(self) -> 'float':
        """float: 'MinimumClampLoadAtTheOpeningLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumClampLoadAtTheOpeningLimit

        if temp is None:
            return None

        return temp

    @property
    def minimum_clamp_load_for_transmitting_transverse_load(self) -> 'float':
        """float: 'MinimumClampLoadForTransmittingTransverseLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumClampLoadForTransmittingTransverseLoad

        if temp is None:
            return None

        return temp

    @property
    def minimum_effective_length_of_engagement(self) -> 'float':
        """float: 'MinimumEffectiveLengthOfEngagement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumEffectiveLengthOfEngagement

        if temp is None:
            return None

        return temp

    @property
    def minimum_length_of_engagement(self) -> 'float':
        """float: 'MinimumLengthOfEngagement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLengthOfEngagement

        if temp is None:
            return None

        return temp

    @property
    def minimum_nominal_diameter(self) -> 'float':
        """float: 'MinimumNominalDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumNominalDiameter

        if temp is None:
            return None

        return temp

    @property
    def minimum_preload(self) -> 'float':
        """float: 'MinimumPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumPreload

        if temp is None:
            return None

        return temp

    @property
    def minimum_required_clamping_force(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumRequiredClampingForce' is the original name of this property."""

        temp = self.wrapped.MinimumRequiredClampingForce

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_required_clamping_force.setter
    def minimum_required_clamping_force(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumRequiredClampingForce = value

    @property
    def minimum_residual_clamp_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumResidualClampLoad' is the original name of this property."""

        temp = self.wrapped.MinimumResidualClampLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_residual_clamp_load.setter
    def minimum_residual_clamp_load(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumResidualClampLoad = value

    @property
    def minimum_residual_clamp_load_maximum_assembly_preload(self) -> 'float':
        """float: 'MinimumResidualClampLoadMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumResidualClampLoadMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def minimum_residual_clamp_load_minimum_assembly_preload(self) -> 'float':
        """float: 'MinimumResidualClampLoadMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumResidualClampLoadMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def minimum_residual_clamp_load_in_assembled_state(self) -> 'float':
        """float: 'MinimumResidualClampLoadInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumResidualClampLoadInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def minimum_stress_in_bending_tension_of_bolt_thread(self) -> 'float':
        """float: 'MinimumStressInBendingTensionOfBoltThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumStressInBendingTensionOfBoltThread

        if temp is None:
            return None

        return temp

    @property
    def number_of_alternating_cycles_during_continuous_loading(self) -> 'float':
        """float: 'NumberOfAlternatingCyclesDuringContinuousLoading' is the original name of this property."""

        temp = self.wrapped.NumberOfAlternatingCyclesDuringContinuousLoading

        if temp is None:
            return None

        return temp

    @number_of_alternating_cycles_during_continuous_loading.setter
    def number_of_alternating_cycles_during_continuous_loading(self, value: 'float'):
        self.wrapped.NumberOfAlternatingCyclesDuringContinuousLoading = float(value) if value else 0.0

    @property
    def number_of_alternating_cycles_during_loading_within_fatigue_range(self) -> 'float':
        """float: 'NumberOfAlternatingCyclesDuringLoadingWithinFatigueRange' is the original name of this property."""

        temp = self.wrapped.NumberOfAlternatingCyclesDuringLoadingWithinFatigueRange

        if temp is None:
            return None

        return temp

    @number_of_alternating_cycles_during_loading_within_fatigue_range.setter
    def number_of_alternating_cycles_during_loading_within_fatigue_range(self, value: 'float'):
        self.wrapped.NumberOfAlternatingCyclesDuringLoadingWithinFatigueRange = float(value) if value else 0.0

    @property
    def number_of_bearing_areas(self) -> 'int':
        """int: 'NumberOfBearingAreas' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfBearingAreas

        if temp is None:
            return None

        return temp

    @property
    def number_of_steps_for_f_mmax_table_a7(self) -> 'int':
        """int: 'NumberOfStepsForFMmaxTableA7' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfStepsForFMmaxTableA7

        if temp is None:
            return None

        return temp

    @property
    def number_of_steps_for_f_mmin_table_a7(self) -> 'int':
        """int: 'NumberOfStepsForFMminTableA7' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfStepsForFMminTableA7

        if temp is None:
            return None

        return temp

    @property
    def operating_temperature_of_bolt(self) -> 'float':
        """float: 'OperatingTemperatureOfBolt' is the original name of this property."""

        temp = self.wrapped.OperatingTemperatureOfBolt

        if temp is None:
            return None

        return temp

    @operating_temperature_of_bolt.setter
    def operating_temperature_of_bolt(self, value: 'float'):
        self.wrapped.OperatingTemperatureOfBolt = float(value) if value else 0.0

    @property
    def operating_temperature_of_clamped_parts(self) -> 'float':
        """float: 'OperatingTemperatureOfClampedParts' is the original name of this property."""

        temp = self.wrapped.OperatingTemperatureOfClampedParts

        if temp is None:
            return None

        return temp

    @operating_temperature_of_clamped_parts.setter
    def operating_temperature_of_clamped_parts(self, value: 'float'):
        self.wrapped.OperatingTemperatureOfClampedParts = float(value) if value else 0.0

    @property
    def parameter_of_circle_equation_mk(self) -> 'float':
        """float: 'ParameterOfCircleEquationMK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParameterOfCircleEquationMK

        if temp is None:
            return None

        return temp

    @property
    def parameter_of_circle_equation_nk(self) -> 'float':
        """float: 'ParameterOfCircleEquationNK' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParameterOfCircleEquationNK

        if temp is None:
            return None

        return temp

    @property
    def permissible_assembly_preload(self) -> 'float':
        """float: 'PermissibleAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def permissible_assembly_preload_assembled_state(self) -> 'float':
        """float: 'PermissibleAssemblyPreloadAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAssemblyPreloadAssembledState

        if temp is None:
            return None

        return temp

    @property
    def permissible_shearing_force_of_bolt(self) -> 'float':
        """float: 'PermissibleShearingForceOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleShearingForceOfBolt

        if temp is None:
            return None

        return temp

    @property
    def permitted_assembly_reduced_stress(self) -> 'float':
        """float: 'PermittedAssemblyReducedStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermittedAssemblyReducedStress

        if temp is None:
            return None

        return temp

    @property
    def plastic_deformation_due_to_embedding(self) -> 'float':
        """float: 'PlasticDeformationDueToEmbedding' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlasticDeformationDueToEmbedding

        if temp is None:
            return None

        return temp

    @property
    def polar_moment_of_resistance(self) -> 'float':
        """float: 'PolarMomentOfResistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PolarMomentOfResistance

        if temp is None:
            return None

        return temp

    @property
    def preload(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Preload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Preload

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def preload_at_opening_limit(self) -> 'float':
        """float: 'PreloadAtOpeningLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PreloadAtOpeningLimit

        if temp is None:
            return None

        return temp

    @property
    def preload_at_room_temperature(self) -> 'float':
        """float: 'PreloadAtRoomTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PreloadAtRoomTemperature

        if temp is None:
            return None

        return temp

    @property
    def preload_in_assembled_state(self) -> 'float':
        """float: 'PreloadInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PreloadInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def present_effective_length_of_engagement(self) -> 'float':
        """float: 'PresentEffectiveLengthOfEngagement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PresentEffectiveLengthOfEngagement

        if temp is None:
            return None

        return temp

    @property
    def present_length_of_engagement(self) -> 'float':
        """float: 'PresentLengthOfEngagement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PresentLengthOfEngagement

        if temp is None:
            return None

        return temp

    @property
    def proportion_of_tightening_torque_in_thread(self) -> 'float':
        """float: 'ProportionOfTighteningTorqueInThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProportionOfTighteningTorqueInThread

        if temp is None:
            return None

        return temp

    @property
    def relieving_load_of_plates(self) -> 'float':
        """float: 'RelievingLoadOfPlates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelievingLoadOfPlates

        if temp is None:
            return None

        return temp

    @property
    def residual_transverse_load(self) -> 'float':
        """float: 'ResidualTransverseLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResidualTransverseLoad

        if temp is None:
            return None

        return temp

    @property
    def resulting_moment_in_clamping_area(self) -> 'float':
        """float: 'ResultingMomentInClampingArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultingMomentInClampingArea

        if temp is None:
            return None

        return temp

    @property
    def shearing_cross_section_of_bolt_thread(self) -> 'float':
        """float: 'ShearingCrossSectionOfBoltThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearingCrossSectionOfBoltThread

        if temp is None:
            return None

        return temp

    @property
    def shearing_cross_section_of_nut_thread(self) -> 'float':
        """float: 'ShearingCrossSectionOfNutThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearingCrossSectionOfNutThread

        if temp is None:
            return None

        return temp

    @property
    def shearing_safety_factor(self) -> 'float':
        """float: 'ShearingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearingSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def slipping_safety_factor(self) -> 'float':
        """float: 'SlippingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlippingSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def slipping_safety_factor_maximum_required_assembly_preload(self) -> 'float':
        """float: 'SlippingSafetyFactorMaximumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlippingSafetyFactorMaximumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def slipping_safety_factor_minimum_required_assembly_preload(self) -> 'float':
        """float: 'SlippingSafetyFactorMinimumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlippingSafetyFactorMinimumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def slipping_safety_factor_in_the_assembled_state(self) -> 'float':
        """float: 'SlippingSafetyFactorInTheAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlippingSafetyFactorInTheAssembledState

        if temp is None:
            return None

        return temp

    @property
    def slipping_safety_factor_in_the_assembled_state_maximum_assembly_preload(self) -> 'float':
        """float: 'SlippingSafetyFactorInTheAssembledStateMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlippingSafetyFactorInTheAssembledStateMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def slipping_safety_factor_in_the_assembled_state_minimum_assembly_preload(self) -> 'float':
        """float: 'SlippingSafetyFactorInTheAssembledStateMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlippingSafetyFactorInTheAssembledStateMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def strength_ratio(self) -> 'float':
        """float: 'StrengthRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrengthRatio

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_endurance_limit_sg(self) -> 'float':
        """float: 'StressAmplitudeOfEnduranceLimitSG' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfEnduranceLimitSG

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_endurance_limit_sg_maximum_assembly_preload(self) -> 'float':
        """float: 'StressAmplitudeOfEnduranceLimitSGMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfEnduranceLimitSGMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_endurance_limit_sg_minimum_assembly_preload(self) -> 'float':
        """float: 'StressAmplitudeOfEnduranceLimitSGMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfEnduranceLimitSGMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_endurance_limit_sv(self) -> 'float':
        """float: 'StressAmplitudeOfEnduranceLimitSV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfEnduranceLimitSV

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_fatigue_strength_sg(self) -> 'float':
        """float: 'StressAmplitudeOfFatigueStrengthSG' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfFatigueStrengthSG

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_fatigue_strength_sg_maximum_assembly_preload(self) -> 'float':
        """float: 'StressAmplitudeOfFatigueStrengthSGMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfFatigueStrengthSGMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_fatigue_strength_sg_minimum_assembly_preload(self) -> 'float':
        """float: 'StressAmplitudeOfFatigueStrengthSGMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfFatigueStrengthSGMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def stress_amplitude_of_fatigue_strength_sv(self) -> 'float':
        """float: 'StressAmplitudeOfFatigueStrengthSV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitudeOfFatigueStrengthSV

        if temp is None:
            return None

        return temp

    @property
    def stress_in_bending_tension_of_bolt_thread(self) -> 'float':
        """float: 'StressInBendingTensionOfBoltThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressInBendingTensionOfBoltThread

        if temp is None:
            return None

        return temp

    @property
    def stripping_force(self) -> 'float':
        """float: 'StrippingForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrippingForce

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor(self) -> 'float':
        """float: 'SurfacePressureSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_maximum_required_assembly_preload(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorMaximumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorMaximumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_minimum_required_assembly_preload(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorMinimumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorMinimumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_in_assembled_state(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_in_working_state(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_in_the_assembled_state_minimum_required_assembly_preload(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorInTheAssembledStateMinimumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorInTheAssembledStateMinimumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_on_head_side(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorOnHeadSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorOnHeadSide

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_on_head_side_in_working_state(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorOnHeadSideInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorOnHeadSideInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_on_nut_side(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorOnNutSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorOnNutSide

        if temp is None:
            return None

        return temp

    @property
    def surface_pressure_safety_factor_on_nut_side_in_working_state(self) -> 'float':
        """float: 'SurfacePressureSafetyFactorOnNutSideInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePressureSafetyFactorOnNutSideInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def tabular_assembly_preload(self) -> 'float':
        """float: 'TabularAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TabularAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def tabular_tightening_torque(self) -> 'float':
        """float: 'TabularTighteningTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TabularTighteningTorque

        if temp is None:
            return None

        return temp

    @property
    def tensile_stress_due_to_assembly_preload(self) -> 'float':
        """float: 'TensileStressDueToAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TensileStressDueToAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def theoretical_load_factor(self) -> 'float':
        """float: 'TheoreticalLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TheoreticalLoadFactor

        if temp is None:
            return None

        return temp

    @property
    def tightening_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TighteningFactor' is the original name of this property."""

        temp = self.wrapped.TighteningFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tightening_factor.setter
    def tightening_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TighteningFactor = value

    @property
    def tightening_technique(self) -> '_1293.TighteningTechniques':
        """TighteningTechniques: 'TighteningTechnique' is the original name of this property."""

        temp = self.wrapped.TighteningTechnique

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1293.TighteningTechniques)(value) if value is not None else None

    @tightening_technique.setter
    def tightening_technique(self, value: '_1293.TighteningTechniques'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TighteningTechnique = value

    @property
    def tightening_torque(self) -> 'float':
        """float: 'TighteningTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TighteningTorque

        if temp is None:
            return None

        return temp

    @property
    def tightening_torque_maximum_assembly_preload(self) -> 'float':
        """float: 'TighteningTorqueMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TighteningTorqueMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def tightening_torque_minimum_assembly_preload(self) -> 'float':
        """float: 'TighteningTorqueMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TighteningTorqueMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def torsional_stress_in_assembled_state(self) -> 'float':
        """float: 'TorsionalStressInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorsionalStressInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def total_bending_moment(self) -> 'float':
        """float: 'TotalBendingMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBendingMoment

        if temp is None:
            return None

        return temp

    @property
    def total_bending_moment_in_bolt(self) -> 'float':
        """float: 'TotalBendingMomentInBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBendingMomentInBolt

        if temp is None:
            return None

        return temp

    @property
    def total_bending_moment_in_plates(self) -> 'float':
        """float: 'TotalBendingMomentInPlates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBendingMomentInPlates

        if temp is None:
            return None

        return temp

    @property
    def total_bolt_load(self) -> 'float':
        """float: 'TotalBoltLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBoltLoad

        if temp is None:
            return None

        return temp

    @property
    def total_bolt_load_maximum_assembly_preload(self) -> 'float':
        """float: 'TotalBoltLoadMaximumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBoltLoadMaximumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def total_bolt_load_minimum_assembly_preload(self) -> 'float':
        """float: 'TotalBoltLoadMinimumAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBoltLoadMinimumAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def yield_point_safety_factor_in_assembled_state(self) -> 'float':
        """float: 'YieldPointSafetyFactorInAssembledState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YieldPointSafetyFactorInAssembledState

        if temp is None:
            return None

        return temp

    @property
    def yield_point_safety_factor_in_assembled_state_maximum_required_assembly_preload(self) -> 'float':
        """float: 'YieldPointSafetyFactorInAssembledStateMaximumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YieldPointSafetyFactorInAssembledStateMaximumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def yield_point_safety_factor_in_working_state(self) -> 'float':
        """float: 'YieldPointSafetyFactorInWorkingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YieldPointSafetyFactorInWorkingState

        if temp is None:
            return None

        return temp

    @property
    def yield_point_safety_factor_in_working_state_maximum_required_assembly_preload(self) -> 'float':
        """float: 'YieldPointSafetyFactorInWorkingStateMaximumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YieldPointSafetyFactorInWorkingStateMaximumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def yield_point_safety_factor_in_working_state_minimum_required_assembly_preload(self) -> 'float':
        """float: 'YieldPointSafetyFactorInWorkingStateMinimumRequiredAssemblyPreload' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YieldPointSafetyFactorInWorkingStateMinimumRequiredAssemblyPreload

        if temp is None:
            return None

        return temp

    @property
    def bolt(self) -> '_1283.DetailedBoltDesign':
        """DetailedBoltDesign: 'Bolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bolt

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def load_vector(self) -> 'Vector3D':
        """Vector3D: 'LoadVector' is the original name of this property."""

        temp = self.wrapped.LoadVector

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @load_vector.setter
    def load_vector(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.LoadVector = value

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
