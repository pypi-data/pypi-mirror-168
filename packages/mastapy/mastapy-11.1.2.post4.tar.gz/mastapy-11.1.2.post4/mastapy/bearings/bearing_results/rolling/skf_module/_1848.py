"""_1848.py

InitialFill
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1855
from mastapy._internal.python_net import python_net_import

_INITIAL_FILL = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'InitialFill')


__docformat__ = 'restructuredtext en'
__all__ = ('InitialFill',)


class InitialFill(_1855.SKFCalculationResult):
    """InitialFill

    This is a mastapy class.
    """

    TYPE = _INITIAL_FILL

    def __init__(self, instance_to_wrap: 'InitialFill.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ring(self) -> 'float':
        """float: 'Ring' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Ring

        if temp is None:
            return None

        return temp

    @property
    def side(self) -> 'float':
        """float: 'Side' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Side

        if temp is None:
            return None

        return temp
