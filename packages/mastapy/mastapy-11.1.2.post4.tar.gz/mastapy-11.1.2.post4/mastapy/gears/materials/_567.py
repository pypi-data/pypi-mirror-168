"""_567.py

KlingelnbergCycloPalloidConicalGearMaterial
"""


from mastapy._internal import constructor
from mastapy.gears.materials import _560
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'KlingelnbergCycloPalloidConicalGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMaterial',)


class KlingelnbergCycloPalloidConicalGearMaterial(_560.GearMaterial):
    """KlingelnbergCycloPalloidConicalGearMaterial

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MATERIAL

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def specify_allowable_stress_numbers(self) -> 'bool':
        """bool: 'SpecifyAllowableStressNumbers' is the original name of this property."""

        temp = self.wrapped.SpecifyAllowableStressNumbers

        if temp is None:
            return None

        return temp

    @specify_allowable_stress_numbers.setter
    def specify_allowable_stress_numbers(self, value: 'bool'):
        self.wrapped.SpecifyAllowableStressNumbers = bool(value) if value else False

    @property
    def stress_number_bending(self) -> 'float':
        """float: 'StressNumberBending' is the original name of this property."""

        temp = self.wrapped.StressNumberBending

        if temp is None:
            return None

        return temp

    @stress_number_bending.setter
    def stress_number_bending(self, value: 'float'):
        self.wrapped.StressNumberBending = float(value) if value else 0.0

    @property
    def stress_number_contact(self) -> 'float':
        """float: 'StressNumberContact' is the original name of this property."""

        temp = self.wrapped.StressNumberContact

        if temp is None:
            return None

        return temp

    @stress_number_contact.setter
    def stress_number_contact(self, value: 'float'):
        self.wrapped.StressNumberContact = float(value) if value else 0.0

    @property
    def stress_number_static_bending(self) -> 'float':
        """float: 'StressNumberStaticBending' is the original name of this property."""

        temp = self.wrapped.StressNumberStaticBending

        if temp is None:
            return None

        return temp

    @stress_number_static_bending.setter
    def stress_number_static_bending(self, value: 'float'):
        self.wrapped.StressNumberStaticBending = float(value) if value else 0.0

    @property
    def stress_number_static_contact(self) -> 'float':
        """float: 'StressNumberStaticContact' is the original name of this property."""

        temp = self.wrapped.StressNumberStaticContact

        if temp is None:
            return None

        return temp

    @stress_number_static_contact.setter
    def stress_number_static_contact(self, value: 'float'):
        self.wrapped.StressNumberStaticContact = float(value) if value else 0.0
