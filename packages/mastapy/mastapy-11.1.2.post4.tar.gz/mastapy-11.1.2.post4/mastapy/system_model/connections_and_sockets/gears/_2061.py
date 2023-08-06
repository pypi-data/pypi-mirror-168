"""_2061.py

CylindricalGearTeethSocket
"""


from mastapy.system_model.connections_and_sockets import _2027
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTeethSocket',)


class CylindricalGearTeethSocket(_2027.CylindricalSocket):
    """CylindricalGearTeethSocket

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_TEETH_SOCKET

    def __init__(self, instance_to_wrap: 'CylindricalGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
