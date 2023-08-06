"""_2054.py

BevelGearMesh
"""


from mastapy.gears.gear_designs.bevel import _1135
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _916
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel import _925
from mastapy.gears.gear_designs.straight_bevel_diff import _929
from mastapy.gears.gear_designs.spiral_bevel import _933
from mastapy.system_model.connections_and_sockets.gears import _2050
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMesh',)


class BevelGearMesh(_2050.AGMAGleasonConicalGearMesh):
    """BevelGearMesh

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_MESH

    def __init__(self, instance_to_wrap: 'BevelGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_mesh_design(self) -> '_1135.BevelGearMeshDesign':
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
    def bevel_gear_mesh_design(self) -> '_1135.BevelGearMeshDesign':
        """BevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearMeshDesign

        if temp is None:
            return None

        if _1135.BevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to BevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bevel_gear_mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_916.ZerolBevelGearMeshDesign':
        """ZerolBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearMeshDesign

        if temp is None:
            return None

        if _916.ZerolBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_925.StraightBevelGearMeshDesign':
        """StraightBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearMeshDesign

        if temp is None:
            return None

        if _925.StraightBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_929.StraightBevelDiffGearMeshDesign':
        """StraightBevelDiffGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearMeshDesign

        if temp is None:
            return None

        if _929.StraightBevelDiffGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bevel_gear_mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_933.SpiralBevelGearMeshDesign':
        """SpiralBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearMeshDesign

        if temp is None:
            return None

        if _933.SpiralBevelGearMeshDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
