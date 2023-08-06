"""_2087.py

CycloidalDiscInnerSocket
"""


from mastapy.system_model.connections_and_sockets import _2031
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_INNER_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscInnerSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscInnerSocket',)


class CycloidalDiscInnerSocket(_2031.InnerShaftSocketBase):
    """CycloidalDiscInnerSocket

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_INNER_SOCKET

    def __init__(self, instance_to_wrap: 'CycloidalDiscInnerSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
