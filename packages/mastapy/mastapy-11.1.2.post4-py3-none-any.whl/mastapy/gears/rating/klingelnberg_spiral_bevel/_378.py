"""_378.py

KlingelnbergCycloPalloidSpiralBevelGearRating
"""


from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _936
from mastapy._internal import constructor
from mastapy.gears.rating.klingelnberg_conical import _384
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergSpiralBevel', 'KlingelnbergCycloPalloidSpiralBevelGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearRating',)


class KlingelnbergCycloPalloidSpiralBevelGearRating(_384.KlingelnbergCycloPalloidConicalGearRating):
    """KlingelnbergCycloPalloidSpiralBevelGearRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_936.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        """KlingelnbergCycloPalloidSpiralBevelGearDesign: 'KlingelnbergCycloPalloidSpiralBevelGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
