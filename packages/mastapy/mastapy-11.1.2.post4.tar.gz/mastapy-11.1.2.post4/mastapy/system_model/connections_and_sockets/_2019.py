"""_2019.py

BeltConnection
"""


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _2032
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnection',)


class BeltConnection(_2032.InterMountableComponentConnection):
    """BeltConnection

    This is a mastapy class.
    """

    TYPE = _BELT_CONNECTION

    def __init__(self, instance_to_wrap: 'BeltConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def stiffness_of_strand(self) -> 'float':
        """float: 'StiffnessOfStrand' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessOfStrand

        if temp is None:
            return None

        return temp
