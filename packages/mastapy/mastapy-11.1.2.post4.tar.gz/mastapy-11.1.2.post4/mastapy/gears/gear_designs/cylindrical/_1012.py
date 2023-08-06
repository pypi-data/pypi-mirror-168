"""_1012.py

HardenedMaterialProperties
"""


from mastapy._internal import constructor
from mastapy.utility import _1390
from mastapy._internal.python_net import python_net_import

_HARDENED_MATERIAL_PROPERTIES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'HardenedMaterialProperties')


__docformat__ = 'restructuredtext en'
__all__ = ('HardenedMaterialProperties',)


class HardenedMaterialProperties(_1390.IndependentReportablePropertiesBase['HardenedMaterialProperties']):
    """HardenedMaterialProperties

    This is a mastapy class.
    """

    TYPE = _HARDENED_MATERIAL_PROPERTIES

    def __init__(self, instance_to_wrap: 'HardenedMaterialProperties.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def critical_stress(self) -> 'float':
        """float: 'CriticalStress' is the original name of this property."""

        temp = self.wrapped.CriticalStress

        if temp is None:
            return None

        return temp

    @critical_stress.setter
    def critical_stress(self, value: 'float'):
        self.wrapped.CriticalStress = float(value) if value else 0.0

    @property
    def fatigue_sensitivity_to_normal_stress(self) -> 'float':
        """float: 'FatigueSensitivityToNormalStress' is the original name of this property."""

        temp = self.wrapped.FatigueSensitivityToNormalStress

        if temp is None:
            return None

        return temp

    @fatigue_sensitivity_to_normal_stress.setter
    def fatigue_sensitivity_to_normal_stress(self, value: 'float'):
        self.wrapped.FatigueSensitivityToNormalStress = float(value) if value else 0.0
