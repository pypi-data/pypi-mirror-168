"""_519.py

ConceptGearSetRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.concept import _1132
from mastapy.gears.rating.concept import _517, _516
from mastapy.gears.rating import _335
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetRating',)


class ConceptGearSetRating(_335.GearSetRating):
    """ConceptGearSetRating

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_SET_RATING

    def __init__(self, instance_to_wrap: 'ConceptGearSetRating.TYPE'):
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
    def concept_gear_set(self) -> '_1132.ConceptGearSetDesign':
        """ConceptGearSetDesign: 'ConceptGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_ratings(self) -> 'List[_517.ConceptGearRating]':
        """List[ConceptGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_gear_ratings(self) -> 'List[_517.ConceptGearRating]':
        """List[ConceptGearRating]: 'ConceptGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_mesh_ratings(self) -> 'List[_516.ConceptGearMeshRating]':
        """List[ConceptGearMeshRating]: 'ConceptMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptMeshRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
