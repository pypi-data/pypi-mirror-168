"""_2056.py

ConceptGearMesh
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.concept import _1131
from mastapy.system_model.connections_and_sockets.gears import _2064
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMesh',)


class ConceptGearMesh(_2064.GearMesh):
    """ConceptGearMesh

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH

    def __init__(self, instance_to_wrap: 'ConceptGearMesh.TYPE'):
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
    def active_gear_mesh_design(self) -> '_1131.ConceptGearMeshDesign':
        """ConceptGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def concept_gear_mesh_design(self) -> '_1131.ConceptGearMeshDesign':
        """ConceptGearMeshDesign: 'ConceptGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
