"""_2066.py

HypoidGearMesh
"""


from mastapy.gears.gear_designs.hypoid import _949
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _2050
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMesh',)


class HypoidGearMesh(_2050.AGMAGleasonConicalGearMesh):
    """HypoidGearMesh

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_MESH

    def __init__(self, instance_to_wrap: 'HypoidGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_mesh_design(self) -> '_949.HypoidGearMeshDesign':
        """HypoidGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hypoid_gear_mesh_design(self) -> '_949.HypoidGearMeshDesign':
        """HypoidGearMeshDesign: 'HypoidGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
