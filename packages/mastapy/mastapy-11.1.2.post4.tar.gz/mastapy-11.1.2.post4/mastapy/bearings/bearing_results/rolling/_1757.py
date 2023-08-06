"""_1757.py

LoadedBallBearingDutyCycle
"""


from mastapy._internal import constructor
from mastapy.utility.property import _1615
from mastapy.bearings.bearing_results.rolling import _1760
from mastapy.bearings.bearing_results import _1722
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingDutyCycle',)


class LoadedBallBearingDutyCycle(_1722.LoadedRollingBearingDutyCycle):
    """LoadedBallBearingDutyCycle

    This is a mastapy class.
    """

    TYPE = _LOADED_BALL_BEARING_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'LoadedBallBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def track_truncation_safety_factor(self) -> 'float':
        """float: 'TrackTruncationSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TrackTruncationSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def track_truncation_inner_summary(self) -> '_1615.DutyCyclePropertySummaryPercentage[_1760.LoadedBallBearingResults]':
        """DutyCyclePropertySummaryPercentage[LoadedBallBearingResults]: 'TrackTruncationInnerSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TrackTruncationInnerSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1760.LoadedBallBearingResults](temp) if temp is not None else None

    @property
    def track_truncation_outer_summary(self) -> '_1615.DutyCyclePropertySummaryPercentage[_1760.LoadedBallBearingResults]':
        """DutyCyclePropertySummaryPercentage[LoadedBallBearingResults]: 'TrackTruncationOuterSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TrackTruncationOuterSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1760.LoadedBallBearingResults](temp) if temp is not None else None
