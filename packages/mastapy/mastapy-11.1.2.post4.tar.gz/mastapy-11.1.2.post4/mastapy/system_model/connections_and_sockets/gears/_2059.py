"""_2059.py

ConicalGearTeethSocket
"""


from mastapy.system_model.connections_and_sockets.gears import _2065
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearTeethSocket',)


class ConicalGearTeethSocket(_2065.GearTeethSocket):
    """ConicalGearTeethSocket

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_TEETH_SOCKET

    def __init__(self, instance_to_wrap: 'ConicalGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
