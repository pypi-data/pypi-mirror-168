"""_1815.py

LoadedToroidalRollerBearingElement
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1786
from mastapy._internal.python_net import python_net_import

_LOADED_TOROIDAL_ROLLER_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedToroidalRollerBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedToroidalRollerBearingElement',)


class LoadedToroidalRollerBearingElement(_1786.LoadedRollerBearingElement):
    """LoadedToroidalRollerBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_TOROIDAL_ROLLER_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedToroidalRollerBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_angle(self) -> 'float':
        """float: 'ContactAngle' is the original name of this property."""

        temp = self.wrapped.ContactAngle

        if temp is None:
            return None

        return temp

    @contact_angle.setter
    def contact_angle(self, value: 'float'):
        self.wrapped.ContactAngle = float(value) if value else 0.0
