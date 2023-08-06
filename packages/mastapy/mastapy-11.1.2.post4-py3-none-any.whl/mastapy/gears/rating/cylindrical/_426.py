"""_426.py

CylindricalGearFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating import _331
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFlankRating',)


class CylindricalGearFlankRating(_331.GearFlankRating):
    """CylindricalGearFlankRating

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FLANK_RATING

    def __init__(self, instance_to_wrap: 'CylindricalGearFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worst_dynamic_factor(self) -> 'float':
        """float: 'WorstDynamicFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorstDynamicFactor

        if temp is None:
            return None

        return temp

    @property
    def worst_face_load_factor_contact(self) -> 'float':
        """float: 'WorstFaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorstFaceLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def worst_load_sharing_factor(self) -> 'float':
        """float: 'WorstLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorstLoadSharingFactor

        if temp is None:
            return None

        return temp
