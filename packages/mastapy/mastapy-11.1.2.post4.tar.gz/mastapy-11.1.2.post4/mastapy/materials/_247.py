"""_247.py

MaterialsSettings
"""


from typing import List

from mastapy.utility.property import _1618
from mastapy.materials import _248
from mastapy._internal import constructor, conversion
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_MATERIALS_SETTINGS = python_net_import('SMT.MastaAPI.Materials', 'MaterialsSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialsSettings',)


class MaterialsSettings(_1395.PerMachineSettings):
    """MaterialsSettings

    This is a mastapy class.
    """

    TYPE = _MATERIALS_SETTINGS

    def __init__(self, instance_to_wrap: 'MaterialsSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def available_material_standards(self) -> 'List[_1618.EnumWithBool[_248.MaterialStandards]]':
        """List[EnumWithBool[MaterialStandards]]: 'AvailableMaterialStandards' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AvailableMaterialStandards

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
