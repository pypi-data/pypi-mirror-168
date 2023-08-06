"""_1314.py

Eigenmode
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_EIGENMODE = python_net_import('SMT.MastaAPI.MathUtility', 'Eigenmode')


__docformat__ = 'restructuredtext en'
__all__ = ('Eigenmode',)


class Eigenmode(_0.APIBase):
    """Eigenmode

    This is a mastapy class.
    """

    TYPE = _EIGENMODE

    def __init__(self, instance_to_wrap: 'Eigenmode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def frequency(self) -> 'float':
        """float: 'Frequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Frequency

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp
