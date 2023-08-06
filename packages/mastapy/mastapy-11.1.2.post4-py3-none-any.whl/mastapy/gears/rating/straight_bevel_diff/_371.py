"""_371.py

StraightBevelDiffGearRating
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.straight_bevel_diff import _928
from mastapy.gears.rating.conical import _506
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevelDiff', 'StraightBevelDiffGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearRating',)


class StraightBevelDiffGearRating(_506.ConicalGearRating):
    """StraightBevelDiffGearRating

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_RATING

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cycles_to_fail(self) -> 'float':
        """float: 'CyclesToFail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CyclesToFail

        if temp is None:
            return None

        return temp

    @property
    def cycles_to_fail_bending(self) -> 'float':
        """float: 'CyclesToFailBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CyclesToFailBending

        if temp is None:
            return None

        return temp

    @property
    def cycles_to_fail_contact(self) -> 'float':
        """float: 'CyclesToFailContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CyclesToFailContact

        if temp is None:
            return None

        return temp

    @property
    def time_to_fail(self) -> 'float':
        """float: 'TimeToFail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeToFail

        if temp is None:
            return None

        return temp

    @property
    def time_to_fail_bending(self) -> 'float':
        """float: 'TimeToFailBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeToFailBending

        if temp is None:
            return None

        return temp

    @property
    def time_to_fail_contact(self) -> 'float':
        """float: 'TimeToFailContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeToFailContact

        if temp is None:
            return None

        return temp

    @property
    def straight_bevel_diff_gear(self) -> '_928.StraightBevelDiffGearDesign':
        """StraightBevelDiffGearDesign: 'StraightBevelDiffGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
