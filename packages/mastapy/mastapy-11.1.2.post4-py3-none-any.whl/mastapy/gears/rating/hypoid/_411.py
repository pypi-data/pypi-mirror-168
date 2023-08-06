"""_411.py

HypoidGearRating
"""


from mastapy.gears.gear_designs.hypoid import _948
from mastapy._internal import constructor
from mastapy.gears.rating.agma_gleason_conical import _532
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid', 'HypoidGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearRating',)


class HypoidGearRating(_532.AGMAGleasonConicalGearRating):
    """HypoidGearRating

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_RATING

    def __init__(self, instance_to_wrap: 'HypoidGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hypoid_gear(self) -> '_948.HypoidGearDesign':
        """HypoidGearDesign: 'HypoidGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
