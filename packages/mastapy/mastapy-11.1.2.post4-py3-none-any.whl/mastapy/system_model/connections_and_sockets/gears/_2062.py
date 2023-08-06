"""_2062.py

FaceGearMesh
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.face import _954
from mastapy.system_model.connections_and_sockets.gears import _2064
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMesh',)


class FaceGearMesh(_2064.GearMesh):
    """FaceGearMesh

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_MESH

    def __init__(self, instance_to_wrap: 'FaceGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pinion_drop_angle(self) -> 'float':
        """float: 'PinionDropAngle' is the original name of this property."""

        temp = self.wrapped.PinionDropAngle

        if temp is None:
            return None

        return temp

    @pinion_drop_angle.setter
    def pinion_drop_angle(self, value: 'float'):
        self.wrapped.PinionDropAngle = float(value) if value else 0.0

    @property
    def wheel_drop_angle(self) -> 'float':
        """float: 'WheelDropAngle' is the original name of this property."""

        temp = self.wrapped.WheelDropAngle

        if temp is None:
            return None

        return temp

    @wheel_drop_angle.setter
    def wheel_drop_angle(self, value: 'float'):
        self.wrapped.WheelDropAngle = float(value) if value else 0.0

    @property
    def active_gear_mesh_design(self) -> '_954.FaceGearMeshDesign':
        """FaceGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_gear_mesh_design(self) -> '_954.FaceGearMeshDesign':
        """FaceGearMeshDesign: 'FaceGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
