"""_1830.py

RollingBearingSpeedResults
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_SPEED_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'RollingBearingSpeedResults')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingSpeedResults',)


class RollingBearingSpeedResults(_0.APIBase):
    """RollingBearingSpeedResults

    This is a mastapy class.
    """

    TYPE = _ROLLING_BEARING_SPEED_RESULTS

    def __init__(self, instance_to_wrap: 'RollingBearingSpeedResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_element_passing_order(self) -> 'float':
        """float: 'AbsoluteElementPassingOrder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteElementPassingOrder

        if temp is None:
            return None

        return temp

    @property
    def element_spin_order(self) -> 'float':
        """float: 'ElementSpinOrder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElementSpinOrder

        if temp is None:
            return None

        return temp

    @property
    def fundamental_train_order(self) -> 'float':
        """float: 'FundamentalTrainOrder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FundamentalTrainOrder

        if temp is None:
            return None

        return temp

    @property
    def inner_race_element_passing_order(self) -> 'float':
        """float: 'InnerRaceElementPassingOrder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerRaceElementPassingOrder

        if temp is None:
            return None

        return temp

    @property
    def outer_race_element_passing_order(self) -> 'float':
        """float: 'OuterRaceElementPassingOrder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterRaceElementPassingOrder

        if temp is None:
            return None

        return temp
