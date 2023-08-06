"""_2468.py

ConicalGearMeshSystemDeflection
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.conical import _1104, _1109, _1114
from mastapy.system_model.connections_and_sockets.gears import (
    _2058, _2050, _2052, _2054,
    _2066, _2069, _2070, _2071,
    _2074, _2076, _2078, _2082
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2470, _2440, _2447, _2448,
    _2449, _2452, _2509, _2514,
    _2517, _2520, _2553, _2559,
    _2562, _2563, _2564, _2585,
    _2503
)
from mastapy.gears.ltca.conical import _836
from mastapy.gears.gear_designs.zerol_bevel import _916
from mastapy.gears.gear_designs.straight_bevel import _925
from mastapy.gears.gear_designs.straight_bevel_diff import _929
from mastapy.gears.gear_designs.spiral_bevel import _933
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _937
from mastapy.gears.gear_designs.klingelnberg_hypoid import _941
from mastapy.gears.gear_designs.klingelnberg_conical import _945
from mastapy.gears.gear_designs.hypoid import _949
from mastapy.gears.gear_designs.bevel import _1135
from mastapy.gears.gear_designs.agma_gleason_conical import _1148
from mastapy.gears.rating.conical import _505
from mastapy.gears.rating.zerol_bevel import _341
from mastapy.gears.rating.straight_bevel import _367
from mastapy.gears.rating.straight_bevel_diff import _370
from mastapy.gears.rating.spiral_bevel import _374
from mastapy.gears.rating.klingelnberg_spiral_bevel import _377
from mastapy.gears.rating.klingelnberg_hypoid import _380
from mastapy.gears.rating.klingelnberg_conical import _383
from mastapy.gears.rating.hypoid import _410
from mastapy.gears.rating.bevel import _520
from mastapy.gears.rating.agma_gleason_conical import _531
from mastapy.system_model.analyses_and_results.power_flows import (
    _3806, _3778, _3785, _3790,
    _3837, _3841, _3844, _3847,
    _3876, _3882, _3885, _3904
)
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConicalGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshSystemDeflection',)


class ConicalGearMeshSystemDeflection(_2503.GearMeshSystemDeflection):
    """ConicalGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_MESH_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ConicalGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_misalignment_in_surface_of_action(self) -> 'float':
        """float: 'AngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularMisalignmentInSurfaceOfAction

        if temp is None:
            return None

        return temp

    @property
    def delta_e(self) -> 'float':
        """float: 'DeltaE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeltaE

        if temp is None:
            return None

        return temp

    @property
    def delta_sigma(self) -> 'float':
        """float: 'DeltaSigma' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeltaSigma

        if temp is None:
            return None

        return temp

    @property
    def delta_xp(self) -> 'float':
        """float: 'DeltaXP' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeltaXP

        if temp is None:
            return None

        return temp

    @property
    def delta_xw(self) -> 'float':
        """float: 'DeltaXW' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeltaXW

        if temp is None:
            return None

        return temp

    @property
    def linear_misalignment_in_surface_of_action(self) -> 'float':
        """float: 'LinearMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearMisalignmentInSurfaceOfAction

        if temp is None:
            return None

        return temp

    @property
    def load_in_line_of_action_from_ltca(self) -> 'float':
        """float: 'LoadInLineOfActionFromLTCA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadInLineOfActionFromLTCA

        if temp is None:
            return None

        return temp

    @property
    def loaded_flank(self) -> '_1104.ActiveConicalFlank':
        """ActiveConicalFlank: 'LoadedFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1104.ActiveConicalFlank)(value) if value is not None else None

    @property
    def pinion_angular_misalignment_in_surface_of_action(self) -> 'float':
        """float: 'PinionAngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionAngularMisalignmentInSurfaceOfAction

        if temp is None:
            return None

        return temp

    @property
    def pinion_torque_for_ltca(self) -> 'float':
        """float: 'PinionTorqueForLTCA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionTorqueForLTCA

        if temp is None:
            return None

        return temp

    @property
    def torque_on_gear_a_due_to_force_in_line_of_action_at_mesh_node(self) -> 'float':
        """float: 'TorqueOnGearADueToForceInLineOfActionAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueOnGearADueToForceInLineOfActionAtMeshNode

        if temp is None:
            return None

        return temp

    @property
    def torque_on_gear_a_due_to_moment_at_mesh_node(self) -> 'float':
        """float: 'TorqueOnGearADueToMomentAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueOnGearADueToMomentAtMeshNode

        if temp is None:
            return None

        return temp

    @property
    def torque_on_gear_b_due_to_force_in_line_of_action_at_mesh_node(self) -> 'float':
        """float: 'TorqueOnGearBDueToForceInLineOfActionAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueOnGearBDueToForceInLineOfActionAtMeshNode

        if temp is None:
            return None

        return temp

    @property
    def torque_on_gear_b_due_to_moment_at_mesh_node(self) -> 'float':
        """float: 'TorqueOnGearBDueToMomentAtMeshNode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueOnGearBDueToMomentAtMeshNode

        if temp is None:
            return None

        return temp

    @property
    def wheel_angular_misalignment_in_surface_of_action(self) -> 'float':
        """float: 'WheelAngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelAngularMisalignmentInSurfaceOfAction

        if temp is None:
            return None

        return temp

    @property
    def connection_design(self) -> '_2058.ConicalGearMesh':
        """ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2058.ConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_2050.AGMAGleasonConicalGearMesh':
        """AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2050.AGMAGleasonConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_2052.BevelDifferentialGearMesh':
        """BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2052.BevelDifferentialGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_2054.BevelGearMesh':
        """BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2054.BevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_2066.HypoidGearMesh':
        """HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2066.HypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2069.KlingelnbergCycloPalloidConicalGearMesh':
        """KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2069.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2070.KlingelnbergCycloPalloidHypoidGearMesh':
        """KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2070.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2071.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        """KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2071.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_2074.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2074.SpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_2076.StraightBevelDiffGearMesh':
        """StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2076.StraightBevelDiffGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_2078.StraightBevelGearMesh':
        """StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2078.StraightBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_2082.ZerolBevelGearMesh':
        """ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2082.ZerolBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a(self) -> '_2470.ConicalGearSystemDeflection':
        """ConicalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2470.ConicalGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_agma_gleason_conical_gear_system_deflection(self) -> '_2440.AGMAGleasonConicalGearSystemDeflection':
        """AGMAGleasonConicalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2440.AGMAGleasonConicalGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AGMAGleasonConicalGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_bevel_differential_gear_system_deflection(self) -> '_2447.BevelDifferentialGearSystemDeflection':
        """BevelDifferentialGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2447.BevelDifferentialGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelDifferentialGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_bevel_differential_planet_gear_system_deflection(self) -> '_2448.BevelDifferentialPlanetGearSystemDeflection':
        """BevelDifferentialPlanetGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2448.BevelDifferentialPlanetGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelDifferentialPlanetGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_bevel_differential_sun_gear_system_deflection(self) -> '_2449.BevelDifferentialSunGearSystemDeflection':
        """BevelDifferentialSunGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2449.BevelDifferentialSunGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelDifferentialSunGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_bevel_gear_system_deflection(self) -> '_2452.BevelGearSystemDeflection':
        """BevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2452.BevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_hypoid_gear_system_deflection(self) -> '_2509.HypoidGearSystemDeflection':
        """HypoidGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2509.HypoidGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to HypoidGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_conical_gear_system_deflection(self) -> '_2514.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        """KlingelnbergCycloPalloidConicalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2514.KlingelnbergCycloPalloidConicalGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidConicalGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(self) -> '_2517.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        """KlingelnbergCycloPalloidHypoidGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2517.KlingelnbergCycloPalloidHypoidGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidHypoidGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(self) -> '_2520.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        """KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2520.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_spiral_bevel_gear_system_deflection(self) -> '_2553.SpiralBevelGearSystemDeflection':
        """SpiralBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2553.SpiralBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to SpiralBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_straight_bevel_diff_gear_system_deflection(self) -> '_2559.StraightBevelDiffGearSystemDeflection':
        """StraightBevelDiffGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2559.StraightBevelDiffGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelDiffGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_straight_bevel_gear_system_deflection(self) -> '_2562.StraightBevelGearSystemDeflection':
        """StraightBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2562.StraightBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_straight_bevel_planet_gear_system_deflection(self) -> '_2563.StraightBevelPlanetGearSystemDeflection':
        """StraightBevelPlanetGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2563.StraightBevelPlanetGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelPlanetGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_straight_bevel_sun_gear_system_deflection(self) -> '_2564.StraightBevelSunGearSystemDeflection':
        """StraightBevelSunGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2564.StraightBevelSunGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelSunGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_of_type_zerol_bevel_gear_system_deflection(self) -> '_2585.ZerolBevelGearSystemDeflection':
        """ZerolBevelGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearA

        if temp is None:
            return None

        if _2585.ZerolBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ZerolBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b(self) -> '_2470.ConicalGearSystemDeflection':
        """ConicalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2470.ConicalGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_agma_gleason_conical_gear_system_deflection(self) -> '_2440.AGMAGleasonConicalGearSystemDeflection':
        """AGMAGleasonConicalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2440.AGMAGleasonConicalGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AGMAGleasonConicalGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_bevel_differential_gear_system_deflection(self) -> '_2447.BevelDifferentialGearSystemDeflection':
        """BevelDifferentialGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2447.BevelDifferentialGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelDifferentialGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_bevel_differential_planet_gear_system_deflection(self) -> '_2448.BevelDifferentialPlanetGearSystemDeflection':
        """BevelDifferentialPlanetGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2448.BevelDifferentialPlanetGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelDifferentialPlanetGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_bevel_differential_sun_gear_system_deflection(self) -> '_2449.BevelDifferentialSunGearSystemDeflection':
        """BevelDifferentialSunGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2449.BevelDifferentialSunGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelDifferentialSunGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_bevel_gear_system_deflection(self) -> '_2452.BevelGearSystemDeflection':
        """BevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2452.BevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_hypoid_gear_system_deflection(self) -> '_2509.HypoidGearSystemDeflection':
        """HypoidGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2509.HypoidGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to HypoidGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_conical_gear_system_deflection(self) -> '_2514.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        """KlingelnbergCycloPalloidConicalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2514.KlingelnbergCycloPalloidConicalGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidConicalGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(self) -> '_2517.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        """KlingelnbergCycloPalloidHypoidGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2517.KlingelnbergCycloPalloidHypoidGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidHypoidGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(self) -> '_2520.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        """KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2520.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_spiral_bevel_gear_system_deflection(self) -> '_2553.SpiralBevelGearSystemDeflection':
        """SpiralBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2553.SpiralBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to SpiralBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_straight_bevel_diff_gear_system_deflection(self) -> '_2559.StraightBevelDiffGearSystemDeflection':
        """StraightBevelDiffGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2559.StraightBevelDiffGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelDiffGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_straight_bevel_gear_system_deflection(self) -> '_2562.StraightBevelGearSystemDeflection':
        """StraightBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2562.StraightBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_straight_bevel_planet_gear_system_deflection(self) -> '_2563.StraightBevelPlanetGearSystemDeflection':
        """StraightBevelPlanetGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2563.StraightBevelPlanetGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelPlanetGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_straight_bevel_sun_gear_system_deflection(self) -> '_2564.StraightBevelSunGearSystemDeflection':
        """StraightBevelSunGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2564.StraightBevelSunGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelSunGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_of_type_zerol_bevel_gear_system_deflection(self) -> '_2585.ZerolBevelGearSystemDeflection':
        """ZerolBevelGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearB

        if temp is None:
            return None

        if _2585.ZerolBevelGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ZerolBevelGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ltca_results(self) -> '_836.ConicalMeshLoadDistributionAnalysis':
        """ConicalMeshLoadDistributionAnalysis: 'LTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LTCAResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design(self) -> '_1109.ConicalGearMeshDesign':
        """ConicalGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _1109.ConicalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to ConicalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_916.ZerolBevelGearMeshDesign':
        """ZerolBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _916.ZerolBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_925.StraightBevelGearMeshDesign':
        """StraightBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _925.StraightBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_929.StraightBevelDiffGearMeshDesign':
        """StraightBevelDiffGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _929.StraightBevelDiffGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_933.SpiralBevelGearMeshDesign':
        """SpiralBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _933.SpiralBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_937.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _937.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_941.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        """KlingelnbergCycloPalloidHypoidGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _941.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_945.KlingelnbergConicalGearMeshDesign':
        """KlingelnbergConicalGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _945.KlingelnbergConicalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_hypoid_gear_mesh_design(self) -> '_949.HypoidGearMeshDesign':
        """HypoidGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _949.HypoidGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to HypoidGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_bevel_gear_mesh_design(self) -> '_1135.BevelGearMeshDesign':
        """BevelGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _1135.BevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to BevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_design_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_1148.AGMAGleasonConicalGearMeshDesign':
        """AGMAGleasonConicalGearMeshDesign: 'MeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshDesign

        if temp is None:
            return None

        if _1148.AGMAGleasonConicalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_design to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_node_misalignments_pinion(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MeshNodeMisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshNodeMisalignmentsPinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_node_misalignments_total(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MeshNodeMisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshNodeMisalignmentsTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_node_misalignments_wheel(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MeshNodeMisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshNodeMisalignmentsWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_pinion(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsPinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_total(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_wheel(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_pinion(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_total(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_wheel(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating(self) -> '_505.ConicalGearMeshRating':
        """ConicalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _505.ConicalGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_zerol_bevel_gear_mesh_rating(self) -> '_341.ZerolBevelGearMeshRating':
        """ZerolBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _341.ZerolBevelGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_straight_bevel_gear_mesh_rating(self) -> '_367.StraightBevelGearMeshRating':
        """StraightBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _367.StraightBevelGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_straight_bevel_diff_gear_mesh_rating(self) -> '_370.StraightBevelDiffGearMeshRating':
        """StraightBevelDiffGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _370.StraightBevelDiffGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelDiffGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_spiral_bevel_gear_mesh_rating(self) -> '_374.SpiralBevelGearMeshRating':
        """SpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _374.SpiralBevelGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(self) -> '_377.KlingelnbergCycloPalloidSpiralBevelGearMeshRating':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _377.KlingelnbergCycloPalloidSpiralBevelGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidSpiralBevelGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(self) -> '_380.KlingelnbergCycloPalloidHypoidGearMeshRating':
        """KlingelnbergCycloPalloidHypoidGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _380.KlingelnbergCycloPalloidHypoidGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidHypoidGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_rating(self) -> '_383.KlingelnbergCycloPalloidConicalGearMeshRating':
        """KlingelnbergCycloPalloidConicalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _383.KlingelnbergCycloPalloidConicalGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidConicalGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_hypoid_gear_mesh_rating(self) -> '_410.HypoidGearMeshRating':
        """HypoidGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _410.HypoidGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to HypoidGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_bevel_gear_mesh_rating(self) -> '_520.BevelGearMeshRating':
        """BevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _520.BevelGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to BevelGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_of_type_agma_gleason_conical_gear_mesh_rating(self) -> '_531.AGMAGleasonConicalGearMeshRating':
        """AGMAGleasonConicalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        if _531.AGMAGleasonConicalGearMeshRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rating to AGMAGleasonConicalGearMeshRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[ConicalGearMeshSystemDeflection]':
        """List[ConicalGearMeshSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_flow_results(self) -> '_3806.ConicalGearMeshPowerFlow':
        """ConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3806.ConicalGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ConicalGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_agma_gleason_conical_gear_mesh_power_flow(self) -> '_3778.AGMAGleasonConicalGearMeshPowerFlow':
        """AGMAGleasonConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3778.AGMAGleasonConicalGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to AGMAGleasonConicalGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_bevel_differential_gear_mesh_power_flow(self) -> '_3785.BevelDifferentialGearMeshPowerFlow':
        """BevelDifferentialGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3785.BevelDifferentialGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BevelDifferentialGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_bevel_gear_mesh_power_flow(self) -> '_3790.BevelGearMeshPowerFlow':
        """BevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3790.BevelGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BevelGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_hypoid_gear_mesh_power_flow(self) -> '_3837.HypoidGearMeshPowerFlow':
        """HypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3837.HypoidGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to HypoidGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(self) -> '_3841.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        """KlingelnbergCycloPalloidConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3841.KlingelnbergCycloPalloidConicalGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidConicalGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(self) -> '_3844.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        """KlingelnbergCycloPalloidHypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3844.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidHypoidGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(self) -> '_3847.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3847.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_spiral_bevel_gear_mesh_power_flow(self) -> '_3876.SpiralBevelGearMeshPowerFlow':
        """SpiralBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3876.SpiralBevelGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to SpiralBevelGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_straight_bevel_diff_gear_mesh_power_flow(self) -> '_3882.StraightBevelDiffGearMeshPowerFlow':
        """StraightBevelDiffGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3882.StraightBevelDiffGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelDiffGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_straight_bevel_gear_mesh_power_flow(self) -> '_3885.StraightBevelGearMeshPowerFlow':
        """StraightBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3885.StraightBevelGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results_of_type_zerol_bevel_gear_mesh_power_flow(self) -> '_3904.ZerolBevelGearMeshPowerFlow':
        """ZerolBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3904.ZerolBevelGearMeshPowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ZerolBevelGearMeshPowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
