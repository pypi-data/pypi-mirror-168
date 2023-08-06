"""_2291.py

PlanetaryGearSet
"""


from typing import List

from mastapy.system_model.part_model.gears import _2274, _2276, _2275
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSet',)


class PlanetaryGearSet(_2275.CylindricalGearSet):
    """PlanetaryGearSet

    This is a mastapy class.
    """

    TYPE = _PLANETARY_GEAR_SET

    def __init__(self, instance_to_wrap: 'PlanetaryGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def annuluses(self) -> 'List[_2274.CylindricalGear]':
        """List[CylindricalGear]: 'Annuluses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Annuluses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planets(self) -> 'List[_2276.CylindricalPlanetGear]':
        """List[CylindricalPlanetGear]: 'Planets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def suns(self) -> 'List[_2274.CylindricalGear]':
        """List[CylindricalGear]: 'Suns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Suns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def add_annulus(self) -> '_2274.CylindricalGear':
        """ 'AddAnnulus' is the original name of this method.

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        """

        method_result = self.wrapped.AddAnnulus()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def add_planet(self) -> '_2274.CylindricalGear':
        """ 'AddPlanet' is the original name of this method.

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        """

        method_result = self.wrapped.AddPlanet()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def add_sun(self) -> '_2274.CylindricalGear':
        """ 'AddSun' is the original name of this method.

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        """

        method_result = self.wrapped.AddSun()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def set_number_of_planets(self, amount: 'int'):
        """ 'SetNumberOfPlanets' is the original name of this method.

        Args:
            amount (int)
        """

        amount = int(amount)
        self.wrapped.SetNumberOfPlanets(amount if amount else 0)
