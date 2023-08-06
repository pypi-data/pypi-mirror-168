"""_1740.py

LoadedAngularContactBallBearingElement
"""


from mastapy.bearings.bearing_results.rolling import _1758
from mastapy._internal.python_net import python_net_import

_LOADED_ANGULAR_CONTACT_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedAngularContactBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedAngularContactBallBearingElement',)


class LoadedAngularContactBallBearingElement(_1758.LoadedBallBearingElement):
    """LoadedAngularContactBallBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_ANGULAR_CONTACT_BALL_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedAngularContactBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
