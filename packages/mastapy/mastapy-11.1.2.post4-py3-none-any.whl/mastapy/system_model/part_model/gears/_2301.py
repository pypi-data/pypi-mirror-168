"""_2301.py

WormGearSet
"""


from typing import List

from mastapy.gears.gear_designs.worm import _922
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2300, _2281
from mastapy.system_model.connections_and_sockets.gears import _2080
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSet',)


class WormGearSet(_2281.GearSet):
    """WormGearSet

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_SET

    def __init__(self, instance_to_wrap: 'WormGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self) -> '_922.WormGearSetDesign':
        """WormGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_set_design(self) -> '_922.WormGearSetDesign':
        """WormGearSetDesign: 'WormGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSetDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gears(self) -> 'List[_2300.WormGear]':
        """List[WormGear]: 'WormGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_meshes(self) -> 'List[_2080.WormGearMesh]':
        """List[WormGearMesh]: 'WormMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
