"""_507.py

ConicalGearSetDutyCycleRating
"""


from typing import List

from mastapy.gears.rating.conical import _510
from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _334
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalGearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSetDutyCycleRating',)


class ConicalGearSetDutyCycleRating(_334.GearSetDutyCycleRating):
    """ConicalGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_SET_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'ConicalGearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_mesh_duty_cycle_ratings(self) -> 'List[_510.ConicalMeshDutyCycleRating]':
        """List[ConicalMeshDutyCycleRating]: 'GearMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMeshDutyCycleRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def conical_mesh_duty_cycle_ratings(self) -> 'List[_510.ConicalMeshDutyCycleRating]':
        """List[ConicalMeshDutyCycleRating]: 'ConicalMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConicalMeshDutyCycleRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
