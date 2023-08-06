"""_2043.py

RollingRingConnection
"""


from mastapy.system_model.connections_and_sockets import _2032
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnection',)


class RollingRingConnection(_2032.InterMountableComponentConnection):
    """RollingRingConnection

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_CONNECTION

    def __init__(self, instance_to_wrap: 'RollingRingConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
