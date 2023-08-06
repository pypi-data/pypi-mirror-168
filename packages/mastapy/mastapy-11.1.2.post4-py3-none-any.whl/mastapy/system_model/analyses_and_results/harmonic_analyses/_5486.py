"""_5486.py

GearMeshExcitationDetail
"""


from mastapy.system_model.analyses_and_results.system_deflections import (
    _2503, _2438, _2445, _2450,
    _2464, _2468, _2483, _2484,
    _2485, _2498, _2507, _2512,
    _2515, _2518, _2551, _2557,
    _2560, _2580, _2583
)
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6699
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5438, _5413
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'GearMeshExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshExcitationDetail',)


class GearMeshExcitationDetail(_5413.AbstractPeriodicExcitationDetail):
    """GearMeshExcitationDetail

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'GearMeshExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_mesh(self) -> '_2503.GearMeshSystemDeflection':
        """GearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2503.GearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to GearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2438.AGMAGleasonConicalGearMeshSystemDeflection':
        """AGMAGleasonConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2438.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2445.BevelDifferentialGearMeshSystemDeflection':
        """BevelDifferentialGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2445.BevelDifferentialGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_bevel_gear_mesh_system_deflection(self) -> '_2450.BevelGearMeshSystemDeflection':
        """BevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2450.BevelGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to BevelGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_concept_gear_mesh_system_deflection(self) -> '_2464.ConceptGearMeshSystemDeflection':
        """ConceptGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2464.ConceptGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ConceptGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_conical_gear_mesh_system_deflection(self) -> '_2468.ConicalGearMeshSystemDeflection':
        """ConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2468.ConicalGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ConicalGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2483.CylindricalGearMeshSystemDeflection':
        """CylindricalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2483.CylindricalGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2484.CylindricalGearMeshSystemDeflectionTimestep':
        """CylindricalGearMeshSystemDeflectionTimestep: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2484.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2485.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        """CylindricalGearMeshSystemDeflectionWithLTCAResults: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2485.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_face_gear_mesh_system_deflection(self) -> '_2498.FaceGearMeshSystemDeflection':
        """FaceGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2498.FaceGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to FaceGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2507.HypoidGearMeshSystemDeflection':
        """HypoidGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2507.HypoidGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to HypoidGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2512.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        """KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2512.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2515.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        """KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2515.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2518.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2518.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2551.SpiralBevelGearMeshSystemDeflection':
        """SpiralBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2551.SpiralBevelGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2557.StraightBevelDiffGearMeshSystemDeflection':
        """StraightBevelDiffGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2557.StraightBevelDiffGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2560.StraightBevelGearMeshSystemDeflection':
        """StraightBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2560.StraightBevelGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_worm_gear_mesh_system_deflection(self) -> '_2580.WormGearMeshSystemDeflection':
        """WormGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2580.WormGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to WormGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2583.ZerolBevelGearMeshSystemDeflection':
        """ZerolBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMesh

        if temp is None:
            return None

        if _2583.ZerolBevelGearMeshSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def get_compliance_and_force_data(self, excitation_type: '_6699.TEExcitationType') -> '_5438.ComplianceAndForceData':
        """ 'GetComplianceAndForceData' is the original name of this method.

        Args:
            excitation_type (mastapy.system_model.analyses_and_results.static_loads.TEExcitationType)

        Returns:
            mastapy.system_model.analyses_and_results.harmonic_analyses.ComplianceAndForceData
        """

        excitation_type = conversion.mp_to_pn_enum(excitation_type)
        method_result = self.wrapped.GetComplianceAndForceData(excitation_type)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
