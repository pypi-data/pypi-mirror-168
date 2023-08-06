"""_2086.py

CycloidalDiscCentralBearingConnection
"""


from mastapy.system_model.connections_and_sockets import _2020
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnection',)


class CycloidalDiscCentralBearingConnection(_2020.CoaxialConnection):
    """CycloidalDiscCentralBearingConnection

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
