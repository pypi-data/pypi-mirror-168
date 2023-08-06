"""_5741.py

AssemblyHarmonicAnalysisOfSingleExcitation
"""


from typing import List

from mastapy.system_model.part_model import _2185, _2224
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6542, _6675
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _5742, _5744, _5747, _5753,
    _5754, _5775, _5757, _5762,
    _5765, _5777, _5779, _5783,
    _5790, _5789, _5791, _5799,
    _5806, _5809, _5810, _5811,
    _5813, _5817, _5820, _5821,
    _5822, _5824, _5826, _5831,
    _5830, _5836, _5839, _5842,
    _5845, _5849, _5853, _5856,
    _5860, _5863, _5734
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'AssemblyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyHarmonicAnalysisOfSingleExcitation',)


class AssemblyHarmonicAnalysisOfSingleExcitation(_5734.AbstractAssemblyHarmonicAnalysisOfSingleExcitation):
    """AssemblyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'AssemblyHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_load_case(self) -> '_6542.AssemblyLoadCase':
        """AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        if _6542.AssemblyLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearings(self) -> 'List[_5742.BearingHarmonicAnalysisOfSingleExcitation]':
        """List[BearingHarmonicAnalysisOfSingleExcitation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def belt_drives(self) -> 'List[_5744.BeltDriveHarmonicAnalysisOfSingleExcitation]':
        """List[BeltDriveHarmonicAnalysisOfSingleExcitation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltDrives

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5747.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelDifferentialGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolted_joints(self) -> 'List[_5753.BoltedJointHarmonicAnalysisOfSingleExcitation]':
        """List[BoltedJointHarmonicAnalysisOfSingleExcitation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltedJoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolts(self) -> 'List[_5754.BoltHarmonicAnalysisOfSingleExcitation]':
        """List[BoltHarmonicAnalysisOfSingleExcitation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bolts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cv_ts(self) -> 'List[_5775.CVTHarmonicAnalysisOfSingleExcitation]':
        """List[CVTHarmonicAnalysisOfSingleExcitation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CVTs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def clutches(self) -> 'List[_5757.ClutchHarmonicAnalysisOfSingleExcitation]':
        """List[ClutchHarmonicAnalysisOfSingleExcitation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clutches

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_couplings(self) -> 'List[_5762.ConceptCouplingHarmonicAnalysisOfSingleExcitation]':
        """List[ConceptCouplingHarmonicAnalysisOfSingleExcitation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5765.ConceptGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[ConceptGearSetHarmonicAnalysisOfSingleExcitation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5777.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation]':
        """List[CycloidalAssemblyHarmonicAnalysisOfSingleExcitation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5779.CycloidalDiscHarmonicAnalysisOfSingleExcitation]':
        """List[CycloidalDiscHarmonicAnalysisOfSingleExcitation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5783.CylindricalGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[CylindricalGearSetHarmonicAnalysisOfSingleExcitation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_parts(self) -> 'List[_5790.FEPartHarmonicAnalysisOfSingleExcitation]':
        """List[FEPartHarmonicAnalysisOfSingleExcitation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gear_sets(self) -> 'List[_5789.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5791.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation]':
        """List[FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5799.HypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[HypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5806.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5809.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mass_discs(self) -> 'List[_5810.MassDiscHarmonicAnalysisOfSingleExcitation]':
        """List[MassDiscHarmonicAnalysisOfSingleExcitation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def measurement_components(self) -> 'List[_5811.MeasurementComponentHarmonicAnalysisOfSingleExcitation]':
        """List[MeasurementComponentHarmonicAnalysisOfSingleExcitation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementComponents

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def oil_seals(self) -> 'List[_5813.OilSealHarmonicAnalysisOfSingleExcitation]':
        """List[OilSealHarmonicAnalysisOfSingleExcitation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilSeals

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5817.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation]':
        """List[PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartToPartShearCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planet_carriers(self) -> 'List[_5820.PlanetCarrierHarmonicAnalysisOfSingleExcitation]':
        """List[PlanetCarrierHarmonicAnalysisOfSingleExcitation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetCarriers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def point_loads(self) -> 'List[_5821.PointLoadHarmonicAnalysisOfSingleExcitation]':
        """List[PointLoadHarmonicAnalysisOfSingleExcitation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_loads(self) -> 'List[_5822.PowerLoadHarmonicAnalysisOfSingleExcitation]':
        """List[PowerLoadHarmonicAnalysisOfSingleExcitation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def ring_pins(self) -> 'List[_5824.RingPinsHarmonicAnalysisOfSingleExcitation]':
        """List[RingPinsHarmonicAnalysisOfSingleExcitation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5826.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation]':
        """List[RollingRingAssemblyHarmonicAnalysisOfSingleExcitation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingRingAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5831.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]':
        """List[ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftHubConnections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shafts(self) -> 'List[_5830.ShaftHarmonicAnalysisOfSingleExcitation]':
        """List[ShaftHarmonicAnalysisOfSingleExcitation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shafts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5836.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spring_dampers(self) -> 'List[_5839.SpringDamperHarmonicAnalysisOfSingleExcitation]':
        """List[SpringDamperHarmonicAnalysisOfSingleExcitation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringDampers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5842.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5845.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def synchronisers(self) -> 'List[_5849.SynchroniserHarmonicAnalysisOfSingleExcitation]':
        """List[SynchroniserHarmonicAnalysisOfSingleExcitation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Synchronisers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def torque_converters(self) -> 'List[_5853.TorqueConverterHarmonicAnalysisOfSingleExcitation]':
        """List[TorqueConverterHarmonicAnalysisOfSingleExcitation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueConverters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5856.UnbalancedMassHarmonicAnalysisOfSingleExcitation]':
        """List[UnbalancedMassHarmonicAnalysisOfSingleExcitation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UnbalancedMasses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5860.WormGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[WormGearSetHarmonicAnalysisOfSingleExcitation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5863.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        """List[ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
