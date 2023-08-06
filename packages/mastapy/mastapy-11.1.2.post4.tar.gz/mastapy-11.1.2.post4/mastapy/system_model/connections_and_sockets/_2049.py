"""_2049.py

SocketConnectionSelection
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SOCKET_CONNECTION_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'SocketConnectionSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('SocketConnectionSelection',)


class SocketConnectionSelection(_0.APIBase):
    """SocketConnectionSelection

    This is a mastapy class.
    """

    TYPE = _SOCKET_CONNECTION_SELECTION

    def __init__(self, instance_to_wrap: 'SocketConnectionSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    def select(self):
        """ 'Select' is the original name of this method."""

        self.wrapped.Select()
