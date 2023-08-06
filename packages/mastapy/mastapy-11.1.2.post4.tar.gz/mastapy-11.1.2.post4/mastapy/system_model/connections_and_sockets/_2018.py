"""_2018.py

BearingOuterSocket
"""


from mastapy.system_model.connections_and_sockets import _2034
from mastapy._internal.python_net import python_net_import

_BEARING_OUTER_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BearingOuterSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingOuterSocket',)


class BearingOuterSocket(_2034.MountableComponentOuterSocket):
    """BearingOuterSocket

    This is a mastapy class.
    """

    TYPE = _BEARING_OUTER_SOCKET

    def __init__(self, instance_to_wrap: 'BearingOuterSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
