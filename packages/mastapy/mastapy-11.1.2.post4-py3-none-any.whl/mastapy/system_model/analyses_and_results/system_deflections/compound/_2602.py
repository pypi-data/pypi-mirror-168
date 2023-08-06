"""_2602.py

AssemblyCompoundSystemDeflection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _47
from mastapy.system_model.part_model import _2185, _2224
from mastapy._internal.cast_exception import CastException
from mastapy.gears.analysis import _1179
from mastapy.shafts import _37
from mastapy.system_model.analyses_and_results.system_deflections import _2441
from mastapy.system_model.analyses_and_results.system_deflections.compound import (
    _2603, _2605, _2608, _2615,
    _2614, _2636, _2616, _2621,
    _2626, _2638, _2640, _2644,
    _2652, _2651, _2653, _2660,
    _2667, _2670, _2671, _2672,
    _2674, _2676, _2681, _2682,
    _2683, _2685, _2687, _2693,
    _2691, _2698, _2699, _2704,
    _2707, _2710, _2714, _2718,
    _2722, _2725, _2595
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSystemDeflection',)


class AssemblyCompoundSystemDeflection(_2595.AbstractAssemblyCompoundSystemDeflection):
    """AssemblyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def overall_duty_cycle_bearing_reliability(self) -> 'float':
        """float: 'OverallDutyCycleBearingReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallDutyCycleBearingReliability

        if temp is None:
            return None

        return temp

    @property
    def overall_duty_cycle_gear_reliability(self) -> 'float':
        """float: 'OverallDutyCycleGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallDutyCycleGearReliability

        if temp is None:
            return None

        return temp

    @property
    def overall_duty_cycle_shaft_reliability(self) -> 'float':
        """float: 'OverallDutyCycleShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallDutyCycleShaftReliability

        if temp is None:
            return None

        return temp

    @property
    def overall_oil_seal_duty_cycle_reliability(self) -> 'float':
        """float: 'OverallOilSealDutyCycleReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallOilSealDutyCycleReliability

        if temp is None:
            return None

        return temp

    @property
    def overall_system_reliability(self) -> 'float':
        """float: 'OverallSystemReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallSystemReliability

        if temp is None:
            return None

        return temp

    @property
    def analysis_settings(self) -> '_47.AnalysisSettingsObjects':
        """AnalysisSettingsObjects: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design(self) -> '_2185.Assembly':
        """Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2185.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2185.Assembly':
        """Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2185.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_for_all_gear_sets(self) -> '_1179.GearSetGroupDutyCycle':
        """GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingForAllGearSets

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        """ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2441.AssemblySystemDeflection]':
        """List[AssemblySystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bearings(self) -> 'List[_2603.BearingCompoundSystemDeflection]':
        """List[BearingCompoundSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def belt_drives(self) -> 'List[_2605.BeltDriveCompoundSystemDeflection]':
        """List[BeltDriveCompoundSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltDrives

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2608.BevelDifferentialGearSetCompoundSystemDeflection]':
        """List[BevelDifferentialGearSetCompoundSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelDifferentialGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolted_joints(self) -> 'List[_2615.BoltedJointCompoundSystemDeflection]':
        """List[BoltedJointCompoundSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltedJoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolts(self) -> 'List[_2614.BoltCompoundSystemDeflection]':
        """List[BoltCompoundSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bolts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cv_ts(self) -> 'List[_2636.CVTCompoundSystemDeflection]':
        """List[CVTCompoundSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CVTs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def clutches(self) -> 'List[_2616.ClutchCompoundSystemDeflection]':
        """List[ClutchCompoundSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clutches

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_couplings(self) -> 'List[_2621.ConceptCouplingCompoundSystemDeflection]':
        """List[ConceptCouplingCompoundSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2626.ConceptGearSetCompoundSystemDeflection]':
        """List[ConceptGearSetCompoundSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_2638.CycloidalAssemblyCompoundSystemDeflection]':
        """List[CycloidalAssemblyCompoundSystemDeflection]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_discs(self) -> 'List[_2640.CycloidalDiscCompoundSystemDeflection]':
        """List[CycloidalDiscCompoundSystemDeflection]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2644.CylindricalGearSetCompoundSystemDeflection]':
        """List[CylindricalGearSetCompoundSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_parts(self) -> 'List[_2652.FEPartCompoundSystemDeflection]':
        """List[FEPartCompoundSystemDeflection]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gear_sets(self) -> 'List[_2651.FaceGearSetCompoundSystemDeflection]':
        """List[FaceGearSetCompoundSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2653.FlexiblePinAssemblyCompoundSystemDeflection]':
        """List[FlexiblePinAssemblyCompoundSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2660.HypoidGearSetCompoundSystemDeflection]':
        """List[HypoidGearSetCompoundSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2667.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]':
        """List[KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2670.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mass_discs(self) -> 'List[_2671.MassDiscCompoundSystemDeflection]':
        """List[MassDiscCompoundSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def measurement_components(self) -> 'List[_2672.MeasurementComponentCompoundSystemDeflection]':
        """List[MeasurementComponentCompoundSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementComponents

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def oil_seals(self) -> 'List[_2674.OilSealCompoundSystemDeflection]':
        """List[OilSealCompoundSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilSeals

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2676.PartToPartShearCouplingCompoundSystemDeflection]':
        """List[PartToPartShearCouplingCompoundSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartToPartShearCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planet_carriers(self) -> 'List[_2681.PlanetCarrierCompoundSystemDeflection]':
        """List[PlanetCarrierCompoundSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetCarriers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def point_loads(self) -> 'List[_2682.PointLoadCompoundSystemDeflection]':
        """List[PointLoadCompoundSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_loads(self) -> 'List[_2683.PowerLoadCompoundSystemDeflection]':
        """List[PowerLoadCompoundSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def ring_pins(self) -> 'List[_2685.RingPinsCompoundSystemDeflection]':
        """List[RingPinsCompoundSystemDeflection]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rolling_bearings(self) -> 'List[_2603.BearingCompoundSystemDeflection]':
        """List[BearingCompoundSystemDeflection]: 'RollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingBearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2687.RollingRingAssemblyCompoundSystemDeflection]':
        """List[RollingRingAssemblyCompoundSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingRingAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2693.ShaftHubConnectionCompoundSystemDeflection]':
        """List[ShaftHubConnectionCompoundSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftHubConnections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shafts(self) -> 'List[_2691.ShaftCompoundSystemDeflection]':
        """List[ShaftCompoundSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shafts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2698.SpiralBevelGearSetCompoundSystemDeflection]':
        """List[SpiralBevelGearSetCompoundSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spring_dampers(self) -> 'List[_2699.SpringDamperCompoundSystemDeflection]':
        """List[SpringDamperCompoundSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringDampers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2704.StraightBevelDiffGearSetCompoundSystemDeflection]':
        """List[StraightBevelDiffGearSetCompoundSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2707.StraightBevelGearSetCompoundSystemDeflection]':
        """List[StraightBevelGearSetCompoundSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def synchronisers(self) -> 'List[_2710.SynchroniserCompoundSystemDeflection]':
        """List[SynchroniserCompoundSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Synchronisers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def torque_converters(self) -> 'List[_2714.TorqueConverterCompoundSystemDeflection]':
        """List[TorqueConverterCompoundSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueConverters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2718.UnbalancedMassCompoundSystemDeflection]':
        """List[UnbalancedMassCompoundSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UnbalancedMasses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2722.WormGearSetCompoundSystemDeflection]':
        """List[WormGearSetCompoundSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2725.ZerolBevelGearSetCompoundSystemDeflection]':
        """List[ZerolBevelGearSetCompoundSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2441.AssemblySystemDeflection]':
        """List[AssemblySystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
