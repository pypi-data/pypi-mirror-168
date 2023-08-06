"""_518.py

ConceptGearSetDutyCycleRating
"""


from mastapy.gears.rating import _334
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Concept', 'ConceptGearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetDutyCycleRating',)


class ConceptGearSetDutyCycleRating(_334.GearSetDutyCycleRating):
    """ConceptGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_SET_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'ConceptGearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
