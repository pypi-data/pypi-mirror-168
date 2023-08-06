"""_1793.py

LoadedSelfAligningBallBearingElement
"""


from mastapy.bearings.bearing_results.rolling import _1758
from mastapy._internal.python_net import python_net_import

_LOADED_SELF_ALIGNING_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedSelfAligningBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedSelfAligningBallBearingElement',)


class LoadedSelfAligningBallBearingElement(_1758.LoadedBallBearingElement):
    """LoadedSelfAligningBallBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_SELF_ALIGNING_BALL_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedSelfAligningBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
