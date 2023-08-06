"""_348.py

WormGearSetRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.worm import _922
from mastapy.gears.rating.worm import _346, _345
from mastapy.gears.rating import _335
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetRating',)


class WormGearSetRating(_335.GearSetRating):
    """WormGearSetRating

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_SET_RATING

    def __init__(self, instance_to_wrap: 'WormGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> 'str':
        """str: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        return temp

    @property
    def worm_gear_set(self) -> '_922.WormGearSetDesign':
        """WormGearSetDesign: 'WormGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_ratings(self) -> 'List[_346.WormGearRating]':
        """List[WormGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

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

    @property
    def worm_mesh_ratings(self) -> 'List[_345.WormGearMeshRating]':
        """List[WormGearMeshRating]: 'WormMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormMeshRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
