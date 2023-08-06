"""_2064.py

GearMesh
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.gear_designs import _912
from mastapy.gears.gear_designs.zerol_bevel import _916
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _921
from mastapy.gears.gear_designs.straight_bevel import _925
from mastapy.gears.gear_designs.straight_bevel_diff import _929
from mastapy.gears.gear_designs.spiral_bevel import _933
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _937
from mastapy.gears.gear_designs.klingelnberg_hypoid import _941
from mastapy.gears.gear_designs.klingelnberg_conical import _945
from mastapy.gears.gear_designs.hypoid import _949
from mastapy.gears.gear_designs.face import _954
from mastapy.gears.gear_designs.cylindrical import _982
from mastapy.gears.gear_designs.conical import _1109
from mastapy.gears.gear_designs.concept import _1131
from mastapy.gears.gear_designs.bevel import _1135
from mastapy.gears.gear_designs.agma_gleason_conical import _1148
from mastapy.system_model.connections_and_sockets import _2032
from mastapy._internal.python_net import python_net_import

_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMesh',)


class GearMesh(_2032.InterMountableComponentConnection):
    """GearMesh

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH

    def __init__(self, instance_to_wrap: 'GearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mesh_efficiency(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MeshEfficiency' is the original name of this property."""

        temp = self.wrapped.MeshEfficiency

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @mesh_efficiency.setter
    def mesh_efficiency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MeshEfficiency = value

    @property
    def use_specified_mesh_stiffness(self) -> 'bool':
        """bool: 'UseSpecifiedMeshStiffness' is the original name of this property."""

        temp = self.wrapped.UseSpecifiedMeshStiffness

        if temp is None:
            return None

        return temp

    @use_specified_mesh_stiffness.setter
    def use_specified_mesh_stiffness(self, value: 'bool'):
        self.wrapped.UseSpecifiedMeshStiffness = bool(value) if value else False

    @property
    def user_specified_mesh_stiffness(self) -> 'float':
        """float: 'UserSpecifiedMeshStiffness' is the original name of this property."""

        temp = self.wrapped.UserSpecifiedMeshStiffness

        if temp is None:
            return None

        return temp

    @user_specified_mesh_stiffness.setter
    def user_specified_mesh_stiffness(self, value: 'float'):
        self.wrapped.UserSpecifiedMeshStiffness = float(value) if value else 0.0

    @property
    def active_gear_mesh_design(self) -> '_912.GearMeshDesign':
        """GearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _912.GearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to GearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_916.ZerolBevelGearMeshDesign':
        """ZerolBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _916.ZerolBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_worm_gear_mesh_design(self) -> '_921.WormGearMeshDesign':
        """WormGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _921.WormGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to WormGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_925.StraightBevelGearMeshDesign':
        """StraightBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _925.StraightBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_929.StraightBevelDiffGearMeshDesign':
        """StraightBevelDiffGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _929.StraightBevelDiffGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_933.SpiralBevelGearMeshDesign':
        """SpiralBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _933.SpiralBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_937.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _937.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_941.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        """KlingelnbergCycloPalloidHypoidGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _941.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_945.KlingelnbergConicalGearMeshDesign':
        """KlingelnbergConicalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _945.KlingelnbergConicalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_hypoid_gear_mesh_design(self) -> '_949.HypoidGearMeshDesign':
        """HypoidGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _949.HypoidGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to HypoidGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_face_gear_mesh_design(self) -> '_954.FaceGearMeshDesign':
        """FaceGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _954.FaceGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to FaceGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_cylindrical_gear_mesh_design(self) -> '_982.CylindricalGearMeshDesign':
        """CylindricalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _982.CylindricalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to CylindricalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_conical_gear_mesh_design(self) -> '_1109.ConicalGearMeshDesign':
        """ConicalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _1109.ConicalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to ConicalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_concept_gear_mesh_design(self) -> '_1131.ConceptGearMeshDesign':
        """ConceptGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _1131.ConceptGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to ConceptGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_bevel_gear_mesh_design(self) -> '_1135.BevelGearMeshDesign':
        """BevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _1135.BevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to BevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_mesh_design_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_1148.AGMAGleasonConicalGearMeshDesign':
        """AGMAGleasonConicalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        if _1148.AGMAGleasonConicalGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
