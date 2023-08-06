"""_382.py

KlingelnbergCycloPalloidHypoidGearSetRating
"""


from typing import List

from mastapy.gears.gear_designs.klingelnberg_hypoid import _942
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.klingelnberg_hypoid import _381, _380
from mastapy.gears.rating.klingelnberg_conical import _385
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergHypoid', 'KlingelnbergCycloPalloidHypoidGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetRating',)


class KlingelnbergCycloPalloidHypoidGearSetRating(_385.KlingelnbergCycloPalloidConicalGearSetRating):
    """KlingelnbergCycloPalloidHypoidGearSetRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_942.KlingelnbergCycloPalloidHypoidGearSetDesign':
        """KlingelnbergCycloPalloidHypoidGearSetDesign: 'KlingelnbergCycloPalloidHypoidGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_ratings(self) -> 'List[_381.KlingelnbergCycloPalloidHypoidGearRating]':
        """List[KlingelnbergCycloPalloidHypoidGearRating]: 'KlingelnbergCycloPalloidHypoidGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_mesh_ratings(self) -> 'List[_380.KlingelnbergCycloPalloidHypoidGearMeshRating]':
        """List[KlingelnbergCycloPalloidHypoidGearMeshRating]: 'KlingelnbergCycloPalloidHypoidMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidMeshRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
