"""_2103.py

TorqueConverterConnection
"""


from mastapy.system_model.connections_and_sockets.couplings import _2097
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnection',)


class TorqueConverterConnection(_2097.CouplingConnection):
    """TorqueConverterConnection

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_CONNECTION

    def __init__(self, instance_to_wrap: 'TorqueConverterConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
