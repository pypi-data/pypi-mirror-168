"""_2083.py

ZerolBevelGearTeethSocket
"""


from mastapy.system_model.connections_and_sockets.gears import _2055
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearTeethSocket',)


class ZerolBevelGearTeethSocket(_2055.BevelGearTeethSocket):
    """ZerolBevelGearTeethSocket

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_TEETH_SOCKET

    def __init__(self, instance_to_wrap: 'ZerolBevelGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
