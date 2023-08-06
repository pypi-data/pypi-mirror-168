"""_2034.py

MountableComponentOuterSocket
"""


from mastapy.system_model.connections_and_sockets import _2035
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_OUTER_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'MountableComponentOuterSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentOuterSocket',)


class MountableComponentOuterSocket(_2035.MountableComponentSocket):
    """MountableComponentOuterSocket

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_OUTER_SOCKET

    def __init__(self, instance_to_wrap: 'MountableComponentOuterSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
