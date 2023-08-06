"""_1345.py

AbstractOptimisable
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_OPTIMISABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'AbstractOptimisable')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractOptimisable',)


class AbstractOptimisable(_0.APIBase):
    """AbstractOptimisable

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_OPTIMISABLE

    def __init__(self, instance_to_wrap: 'AbstractOptimisable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def parameter_1(self) -> 'float':
        """float: 'Parameter1' is the original name of this property."""

        temp = self.wrapped.Parameter1

        if temp is None:
            return None

        return temp

    @parameter_1.setter
    def parameter_1(self, value: 'float'):
        self.wrapped.Parameter1 = float(value) if value else 0.0

    @property
    def parameter_2(self) -> 'float':
        """float: 'Parameter2' is the original name of this property."""

        temp = self.wrapped.Parameter2

        if temp is None:
            return None

        return temp

    @parameter_2.setter
    def parameter_2(self, value: 'float'):
        self.wrapped.Parameter2 = float(value) if value else 0.0
