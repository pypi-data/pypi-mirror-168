"""_2098.py

CouplingSocket
"""


from mastapy.system_model.connections_and_sockets import _2027
from mastapy._internal.python_net import python_net_import

_COUPLING_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingSocket',)


class CouplingSocket(_2027.CylindricalSocket):
    """CouplingSocket

    This is a mastapy class.
    """

    TYPE = _COUPLING_SOCKET

    def __init__(self, instance_to_wrap: 'CouplingSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
