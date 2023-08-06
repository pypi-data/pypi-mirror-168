"""_1372.py

ShortLengthRange
"""


from mastapy._internal import constructor
from mastapy.math_utility import _1295
from mastapy._internal.python_net import python_net_import

_SHORT_LENGTH_RANGE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredRanges', 'ShortLengthRange')


__docformat__ = 'restructuredtext en'
__all__ = ('ShortLengthRange',)


class ShortLengthRange(_1295.Range):
    """ShortLengthRange

    This is a mastapy class.
    """

    TYPE = _SHORT_LENGTH_RANGE

    def __init__(self, instance_to_wrap: 'ShortLengthRange.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum(self) -> 'float':
        """float: 'Maximum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Maximum

        if temp is None:
            return None

        return temp

    @property
    def minimum(self) -> 'float':
        """float: 'Minimum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Minimum

        if temp is None:
            return None

        return temp
