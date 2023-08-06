"""_515.py

ConceptGearMeshDutyCycleRating
"""


from mastapy.gears.rating import _337
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearMeshDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshDutyCycleRating',)


class ConceptGearMeshDutyCycleRating(_337.MeshDutyCycleRating):
    """ConceptGearMeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'ConceptGearMeshDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
