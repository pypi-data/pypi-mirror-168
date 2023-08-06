"""_1762.py

LoadedCrossedRollerBearingElement
"""


from mastapy.bearings.bearing_results.rolling import _1786
from mastapy._internal.python_net import python_net_import

_LOADED_CROSSED_ROLLER_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCrossedRollerBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCrossedRollerBearingElement',)


class LoadedCrossedRollerBearingElement(_1786.LoadedRollerBearingElement):
    """LoadedCrossedRollerBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_CROSSED_ROLLER_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedCrossedRollerBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
