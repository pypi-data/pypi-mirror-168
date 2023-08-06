"""_1843.py

FrictionalMoment
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FRICTIONAL_MOMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'FrictionalMoment')


__docformat__ = 'restructuredtext en'
__all__ = ('FrictionalMoment',)


class FrictionalMoment(_0.APIBase):
    """FrictionalMoment

    This is a mastapy class.
    """

    TYPE = _FRICTIONAL_MOMENT

    def __init__(self, instance_to_wrap: 'FrictionalMoment.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def at_start_2030_degrees_c_and_zero_speed(self) -> 'float':
        """float: 'AtStart2030DegreesCAndZeroSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AtStart2030DegreesCAndZeroSpeed

        if temp is None:
            return None

        return temp

    @property
    def total(self) -> 'float':
        """float: 'Total' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Total

        if temp is None:
            return None

        return temp
