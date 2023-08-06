"""_2041.py

PulleySocket
"""


from mastapy.system_model.connections_and_sockets import _2027
from mastapy._internal.python_net import python_net_import

_PULLEY_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PulleySocket')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySocket',)


class PulleySocket(_2027.CylindricalSocket):
    """PulleySocket

    This is a mastapy class.
    """

    TYPE = _PULLEY_SOCKET

    def __init__(self, instance_to_wrap: 'PulleySocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
