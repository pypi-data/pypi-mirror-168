"""_878.py

GearSetParetoOptimiser
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs import _913
from mastapy.gears.gear_designs.zerol_bevel import _917
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _922
from mastapy.gears.gear_designs.straight_bevel import _926
from mastapy.gears.gear_designs.straight_bevel_diff import _930
from mastapy.gears.gear_designs.spiral_bevel import _934
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _938
from mastapy.gears.gear_designs.klingelnberg_hypoid import _942
from mastapy.gears.gear_designs.klingelnberg_conical import _946
from mastapy.gears.gear_designs.hypoid import _950
from mastapy.gears.gear_designs.face import _958
from mastapy.gears.gear_designs.cylindrical import _990, _1001
from mastapy.gears.gear_designs.conical import _1110
from mastapy.gears.gear_designs.concept import _1132
from mastapy.gears.gear_designs.bevel import _1136
from mastapy.gears.gear_designs.agma_gleason_conical import _1149
from mastapy.gears.gear_set_pareto_optimiser import _872, _877
from mastapy.gears.rating import _327
from mastapy._internal.python_net import python_net_import

_GEAR_SET_PARETO_OPTIMISER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearSetParetoOptimiser')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetParetoOptimiser',)


class GearSetParetoOptimiser(_872.DesignSpaceSearchBase['_327.AbstractGearSetRating', '_877.GearSetOptimiserCandidate']):
    """GearSetParetoOptimiser

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_PARETO_OPTIMISER

    def __init__(self, instance_to_wrap: 'GearSetParetoOptimiser.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_designs_with_gears_which_cannot_be_manufactured_from_cutters(self) -> 'int':
        """int: 'NumberOfDesignsWithGearsWhichCannotBeManufacturedFromCutters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfDesignsWithGearsWhichCannotBeManufacturedFromCutters

        if temp is None:
            return None

        return temp

    @property
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(self) -> 'bool':
        """bool: 'RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase' is the original name of this property."""

        temp = self.wrapped.RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase

        if temp is None:
            return None

        return temp

    @remove_candidates_which_cannot_be_manufactured_with_cutters_from_database.setter
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(self, value: 'bool'):
        self.wrapped.RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase = bool(value) if value else False

    @property
    def remove_candidates_with_warnings(self) -> 'bool':
        """bool: 'RemoveCandidatesWithWarnings' is the original name of this property."""

        temp = self.wrapped.RemoveCandidatesWithWarnings

        if temp is None:
            return None

        return temp

    @remove_candidates_with_warnings.setter
    def remove_candidates_with_warnings(self, value: 'bool'):
        self.wrapped.RemoveCandidatesWithWarnings = bool(value) if value else False

    @property
    def selected_candidate_geometry(self) -> '_913.GearSetDesign':
        """GearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _913.GearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to GearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_zerol_bevel_gear_set_design(self) -> '_917.ZerolBevelGearSetDesign':
        """ZerolBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _917.ZerolBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to ZerolBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_worm_gear_set_design(self) -> '_922.WormGearSetDesign':
        """WormGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _922.WormGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to WormGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_straight_bevel_gear_set_design(self) -> '_926.StraightBevelGearSetDesign':
        """StraightBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _926.StraightBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to StraightBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_straight_bevel_diff_gear_set_design(self) -> '_930.StraightBevelDiffGearSetDesign':
        """StraightBevelDiffGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _930.StraightBevelDiffGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to StraightBevelDiffGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_spiral_bevel_gear_set_design(self) -> '_934.SpiralBevelGearSetDesign':
        """SpiralBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _934.SpiralBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to SpiralBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_938.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        """KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _938.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_942.KlingelnbergCycloPalloidHypoidGearSetDesign':
        """KlingelnbergCycloPalloidHypoidGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _942.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_klingelnberg_conical_gear_set_design(self) -> '_946.KlingelnbergConicalGearSetDesign':
        """KlingelnbergConicalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _946.KlingelnbergConicalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_hypoid_gear_set_design(self) -> '_950.HypoidGearSetDesign':
        """HypoidGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _950.HypoidGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to HypoidGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_face_gear_set_design(self) -> '_958.FaceGearSetDesign':
        """FaceGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _958.FaceGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to FaceGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_cylindrical_gear_set_design(self) -> '_990.CylindricalGearSetDesign':
        """CylindricalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _990.CylindricalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to CylindricalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_cylindrical_planetary_gear_set_design(self) -> '_1001.CylindricalPlanetaryGearSetDesign':
        """CylindricalPlanetaryGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _1001.CylindricalPlanetaryGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_conical_gear_set_design(self) -> '_1110.ConicalGearSetDesign':
        """ConicalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _1110.ConicalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to ConicalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_concept_gear_set_design(self) -> '_1132.ConceptGearSetDesign':
        """ConceptGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _1132.ConceptGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to ConceptGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_bevel_gear_set_design(self) -> '_1136.BevelGearSetDesign':
        """BevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _1136.BevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to BevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_candidate_geometry_of_type_agma_gleason_conical_gear_set_design(self) -> '_1149.AGMAGleasonConicalGearSetDesign':
        """AGMAGleasonConicalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedCandidateGeometry

        if temp is None:
            return None

        if _1149.AGMAGleasonConicalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def all_candidate_gear_sets(self) -> 'List[_913.GearSetDesign]':
        """List[GearSetDesign]: 'AllCandidateGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllCandidateGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def candidate_gear_sets(self) -> 'List[_913.GearSetDesign]':
        """List[GearSetDesign]: 'CandidateGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CandidateGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def add_chart(self):
        """ 'AddChart' is the original name of this method."""

        self.wrapped.AddChart()

    def reset_charts(self):
        """ 'ResetCharts' is the original name of this method."""

        self.wrapped.ResetCharts()
