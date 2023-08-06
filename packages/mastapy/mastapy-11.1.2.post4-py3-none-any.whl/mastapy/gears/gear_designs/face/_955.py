"""_955.py

FaceGearMeshMicroGeometry
"""


from typing import List

from mastapy.gears.gear_designs.face import _959, _954, _956
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _1177
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearMeshMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshMicroGeometry',)


class FaceGearMeshMicroGeometry(_1177.GearMeshImplementationDetail):
    """FaceGearMeshMicroGeometry

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_MESH_MICRO_GEOMETRY

    def __init__(self, instance_to_wrap: 'FaceGearMeshMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_gear_set_micro_geometry(self) -> '_959.FaceGearSetMicroGeometry':
        """FaceGearSetMicroGeometry: 'FaceGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearSetMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_mesh(self) -> '_954.FaceGearMeshDesign':
        """FaceGearMeshDesign: 'FaceMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_gear_micro_geometries(self) -> 'List[_956.FaceGearMicroGeometry]':
        """List[FaceGearMicroGeometry]: 'FaceGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearMicroGeometries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
