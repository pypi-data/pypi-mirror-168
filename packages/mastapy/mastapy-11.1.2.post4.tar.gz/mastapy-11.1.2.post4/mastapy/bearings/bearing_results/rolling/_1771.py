"""_1771.py

LoadedDeepGrooveBallBearingRow
"""


from mastapy.bearings.bearing_results.rolling import _1770, _1761
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_DEEP_GROOVE_BALL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedDeepGrooveBallBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedDeepGrooveBallBearingRow',)


class LoadedDeepGrooveBallBearingRow(_1761.LoadedBallBearingRow):
    """LoadedDeepGrooveBallBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_DEEP_GROOVE_BALL_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedDeepGrooveBallBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1770.LoadedDeepGrooveBallBearingResults':
        """LoadedDeepGrooveBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
