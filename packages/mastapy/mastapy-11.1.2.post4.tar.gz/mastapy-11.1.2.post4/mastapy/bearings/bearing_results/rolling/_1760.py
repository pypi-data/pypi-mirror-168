"""_1760.py

LoadedBallBearingResults
"""


from mastapy.bearings.bearing_results.rolling import _1734, _1834, _1791
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingResults',)


class LoadedBallBearingResults(_1791.LoadedRollingBearingResults):
    """LoadedBallBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_BALL_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedBallBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def friction_model_for_gyroscopic_moment(self) -> '_1734.FrictionModelForGyroscopicMoment':
        """FrictionModelForGyroscopicMoment: 'FrictionModelForGyroscopicMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrictionModelForGyroscopicMoment

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1734.FrictionModelForGyroscopicMoment)(value) if value is not None else None

    @property
    def use_element_contact_angles_for_angular_velocities(self) -> 'bool':
        """bool: 'UseElementContactAnglesForAngularVelocities' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UseElementContactAnglesForAngularVelocities

        if temp is None:
            return None

        return temp

    @property
    def track_truncation(self) -> '_1834.TrackTruncationSafetyFactorResults':
        """TrackTruncationSafetyFactorResults: 'TrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TrackTruncation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
