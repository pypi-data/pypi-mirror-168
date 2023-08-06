"""_345.py

WormGearMeshRating
"""


from typing import List

from mastapy.gears.gear_designs.worm import _921
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _346
from mastapy.gears.rating import _332
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshRating',)


class WormGearMeshRating(_332.GearMeshRating):
    """WormGearMeshRating

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'WormGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worm_gear_mesh(self) -> '_921.WormGearMeshDesign':
        """WormGearMeshDesign: 'WormGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_ratings(self) -> 'List[_346.WormGearRating]':
        """List[WormGearRating]: 'WormGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
