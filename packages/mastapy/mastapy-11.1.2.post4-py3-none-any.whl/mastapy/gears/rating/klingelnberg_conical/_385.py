"""_385.py

KlingelnbergCycloPalloidConicalGearSetRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.conical import _508
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergConical', 'KlingelnbergCycloPalloidConicalGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSetRating',)


class KlingelnbergCycloPalloidConicalGearSetRating(_508.ConicalGearSetRating):
    """KlingelnbergCycloPalloidConicalGearSetRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSetRating.TYPE'):
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
