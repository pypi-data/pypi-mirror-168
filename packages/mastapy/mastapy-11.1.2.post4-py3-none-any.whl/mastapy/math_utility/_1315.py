"""_1315.py

Eigenmodes
"""


from typing import List

from mastapy.math_utility import _1314
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_EIGENMODES = python_net_import('SMT.MastaAPI.MathUtility', 'Eigenmodes')


__docformat__ = 'restructuredtext en'
__all__ = ('Eigenmodes',)


class Eigenmodes(_0.APIBase):
    """Eigenmodes

    This is a mastapy class.
    """

    TYPE = _EIGENMODES

    def __init__(self, instance_to_wrap: 'Eigenmodes.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def items(self) -> 'List[_1314.Eigenmode]':
        """List[Eigenmode]: 'Items' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Items

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
