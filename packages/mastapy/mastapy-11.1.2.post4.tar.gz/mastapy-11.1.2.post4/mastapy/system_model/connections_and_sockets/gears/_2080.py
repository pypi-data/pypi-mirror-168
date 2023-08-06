"""_2080.py

WormGearMesh
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.worm import _921
from mastapy.system_model.connections_and_sockets.gears import _2064
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMesh',)


class WormGearMesh(_2064.GearMesh):
    """WormGearMesh

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH

    def __init__(self, instance_to_wrap: 'WormGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def meshing_angle(self) -> 'float':
        """float: 'MeshingAngle' is the original name of this property."""

        temp = self.wrapped.MeshingAngle

        if temp is None:
            return None

        return temp

    @meshing_angle.setter
    def meshing_angle(self, value: 'float'):
        self.wrapped.MeshingAngle = float(value) if value else 0.0

    @property
    def active_gear_mesh_design(self) -> '_921.WormGearMeshDesign':
        """WormGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_mesh_design(self) -> '_921.WormGearMeshDesign':
        """WormGearMeshDesign: 'WormGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
