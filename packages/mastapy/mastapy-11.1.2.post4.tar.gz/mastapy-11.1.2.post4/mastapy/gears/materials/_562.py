"""_562.py

GearMaterialExpertSystemFactorSettings
"""


from mastapy._internal import constructor
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_GEAR_MATERIAL_EXPERT_SYSTEM_FACTOR_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Materials', 'GearMaterialExpertSystemFactorSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMaterialExpertSystemFactorSettings',)


class GearMaterialExpertSystemFactorSettings(_1395.PerMachineSettings):
    """GearMaterialExpertSystemFactorSettings

    This is a mastapy class.
    """

    TYPE = _GEAR_MATERIAL_EXPERT_SYSTEM_FACTOR_SETTINGS

    def __init__(self, instance_to_wrap: 'GearMaterialExpertSystemFactorSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_damage(self) -> 'float':
        """float: 'MaximumDamage' is the original name of this property."""

        temp = self.wrapped.MaximumDamage

        if temp is None:
            return None

        return temp

    @maximum_damage.setter
    def maximum_damage(self, value: 'float'):
        self.wrapped.MaximumDamage = float(value) if value else 0.0

    @property
    def maximum_safety_factor(self) -> 'float':
        """float: 'MaximumSafetyFactor' is the original name of this property."""

        temp = self.wrapped.MaximumSafetyFactor

        if temp is None:
            return None

        return temp

    @maximum_safety_factor.setter
    def maximum_safety_factor(self, value: 'float'):
        self.wrapped.MaximumSafetyFactor = float(value) if value else 0.0

    @property
    def minimum_damage(self) -> 'float':
        """float: 'MinimumDamage' is the original name of this property."""

        temp = self.wrapped.MinimumDamage

        if temp is None:
            return None

        return temp

    @minimum_damage.setter
    def minimum_damage(self, value: 'float'):
        self.wrapped.MinimumDamage = float(value) if value else 0.0

    @property
    def minimum_safety_factor(self) -> 'float':
        """float: 'MinimumSafetyFactor' is the original name of this property."""

        temp = self.wrapped.MinimumSafetyFactor

        if temp is None:
            return None

        return temp

    @minimum_safety_factor.setter
    def minimum_safety_factor(self, value: 'float'):
        self.wrapped.MinimumSafetyFactor = float(value) if value else 0.0
