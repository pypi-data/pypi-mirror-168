"""_1770.py

LoadedDeepGrooveBallBearingResults
"""


from mastapy.bearings.bearing_results.rolling import _1760
from mastapy._internal.python_net import python_net_import

_LOADED_DEEP_GROOVE_BALL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedDeepGrooveBallBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedDeepGrooveBallBearingResults',)


class LoadedDeepGrooveBallBearingResults(_1760.LoadedBallBearingResults):
    """LoadedDeepGrooveBallBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_DEEP_GROOVE_BALL_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedDeepGrooveBallBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
