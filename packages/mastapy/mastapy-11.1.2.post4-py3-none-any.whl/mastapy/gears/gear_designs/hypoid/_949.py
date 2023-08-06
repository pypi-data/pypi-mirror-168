"""_949.py

HypoidGearMeshDesign
"""


from typing import List

from mastapy.gears.gear_designs.hypoid import _950, _948, _951
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.agma_gleason_conical import _1148
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Hypoid', 'HypoidGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshDesign',)


class HypoidGearMeshDesign(_1148.AGMAGleasonConicalGearMeshDesign):
    """HypoidGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'HypoidGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hypoid_gear_set(self) -> '_950.HypoidGearSetDesign':
        """HypoidGearSetDesign: 'HypoidGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hypoid_gears(self) -> 'List[_948.HypoidGearDesign]':
        """List[HypoidGearDesign]: 'HypoidGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshed_gears(self) -> 'List[_951.HypoidMeshedGearDesign]':
        """List[HypoidMeshedGearDesign]: 'HypoidMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
