"""_758.py

ConicalSetMicroGeometryConfig
"""


from typing import List

from mastapy.gears.manufacturing.bevel import _743, _752, _759
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_CONICAL_SET_MICRO_GEOMETRY_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalSetMicroGeometryConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalSetMicroGeometryConfig',)


class ConicalSetMicroGeometryConfig(_759.ConicalSetMicroGeometryConfigBase):
    """ConicalSetMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE = _CONICAL_SET_MICRO_GEOMETRY_CONFIG

    def __init__(self, instance_to_wrap: 'ConicalSetMicroGeometryConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_micro_geometry_configuration(self) -> 'List[_743.ConicalGearMicroGeometryConfig]':
        """List[ConicalGearMicroGeometryConfig]: 'GearMicroGeometryConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMicroGeometryConfiguration

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshes(self) -> 'List[_752.ConicalMeshMicroGeometryConfig]':
        """List[ConicalMeshMicroGeometryConfig]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Meshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
