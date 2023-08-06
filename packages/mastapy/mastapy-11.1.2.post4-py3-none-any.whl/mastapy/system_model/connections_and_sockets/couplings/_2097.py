"""_2097.py

CouplingConnection
"""


from mastapy.system_model.connections_and_sockets import _2032
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnection',)


class CouplingConnection(_2032.InterMountableComponentConnection):
    """CouplingConnection

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION

    def __init__(self, instance_to_wrap: 'CouplingConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
