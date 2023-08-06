"""_337.py

MeshDutyCycleRating
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _330, _325
from mastapy._internal.python_net import python_net_import

_MESH_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'MeshDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshDutyCycleRating',)


class MeshDutyCycleRating(_325.AbstractGearMeshRating):
    """MeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _MESH_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'MeshDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def energy_loss(self) -> 'float':
        """float: 'EnergyLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EnergyLoss

        if temp is None:
            return None

        return temp

    @property
    def mesh_efficiency(self) -> 'float':
        """float: 'MeshEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshEfficiency

        if temp is None:
            return None

        return temp

    @property
    def total_energy(self) -> 'float':
        """float: 'TotalEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalEnergy

        if temp is None:
            return None

        return temp

    @property
    def gear_duty_cycle_ratings(self) -> 'List[_330.GearDutyCycleRating]':
        """List[GearDutyCycleRating]: 'GearDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
