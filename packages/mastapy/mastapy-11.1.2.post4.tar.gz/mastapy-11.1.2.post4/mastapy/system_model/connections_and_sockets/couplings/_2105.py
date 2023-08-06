"""_2105.py

TorqueConverterTurbineSocket
"""


from mastapy.system_model.connections_and_sockets.couplings import _2098
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterTurbineSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineSocket',)


class TorqueConverterTurbineSocket(_2098.CouplingSocket):
    """TorqueConverterTurbineSocket

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_TURBINE_SOCKET

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
