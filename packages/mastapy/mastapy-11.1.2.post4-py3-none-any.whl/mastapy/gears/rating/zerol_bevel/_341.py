"""_341.py

ZerolBevelGearMeshRating
"""


from typing import List

from mastapy.gears.gear_designs.zerol_bevel import _916
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.zerol_bevel import _342
from mastapy.gears.rating.bevel import _520
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.ZerolBevel', 'ZerolBevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshRating',)


class ZerolBevelGearMeshRating(_520.BevelGearMeshRating):
    """ZerolBevelGearMeshRating

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def zerol_bevel_gear_mesh(self) -> '_916.ZerolBevelGearMeshDesign':
        """ZerolBevelGearMeshDesign: 'ZerolBevelGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def zerol_bevel_gear_ratings(self) -> 'List[_342.ZerolBevelGearRating]':
        """List[ZerolBevelGearRating]: 'ZerolBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
