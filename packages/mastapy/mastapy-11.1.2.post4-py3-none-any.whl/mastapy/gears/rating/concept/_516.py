"""_516.py

ConceptGearMeshRating
"""


from typing import List

from mastapy.gears.gear_designs.concept import _1131
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.concept import _517
from mastapy.gears.rating import _332
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshRating',)


class ConceptGearMeshRating(_332.GearMeshRating):
    """ConceptGearMeshRating

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'ConceptGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def concept_gear_mesh(self) -> '_1131.ConceptGearMeshDesign':
        """ConceptGearMeshDesign: 'ConceptGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

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
