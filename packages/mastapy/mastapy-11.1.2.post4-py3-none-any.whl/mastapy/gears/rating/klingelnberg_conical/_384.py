"""_384.py

KlingelnbergCycloPalloidConicalGearRating
"""


from mastapy.gears.rating.conical import _506
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergConical', 'KlingelnbergCycloPalloidConicalGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearRating',)


class KlingelnbergCycloPalloidConicalGearRating(_506.ConicalGearRating):
    """KlingelnbergCycloPalloidConicalGearRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
