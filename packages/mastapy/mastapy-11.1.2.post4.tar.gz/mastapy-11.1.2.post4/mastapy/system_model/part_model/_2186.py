"""_2186.py

AbstractAssembly
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2195, _2218
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssembly',)


class AbstractAssembly(_2218.Part):
    """AbstractAssembly

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY

    def __init__(self, instance_to_wrap: 'AbstractAssembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mass_of_assembly(self) -> 'float':
        """float: 'MassOfAssembly' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassOfAssembly

        if temp is None:
            return None

        return temp

    @property
    def components_with_unknown_mass_properties(self) -> 'List[_2195.Component]':
        """List[Component]: 'ComponentsWithUnknownMassProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentsWithUnknownMassProperties

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def components_with_zero_mass_properties(self) -> 'List[_2195.Component]':
        """List[Component]: 'ComponentsWithZeroMassProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentsWithZeroMassProperties

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
