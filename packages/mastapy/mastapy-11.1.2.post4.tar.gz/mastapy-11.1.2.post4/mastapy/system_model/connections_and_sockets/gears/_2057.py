"""_2057.py

ConceptGearTeethSocket
"""


from mastapy.system_model.connections_and_sockets.gears import _2065
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearTeethSocket',)


class ConceptGearTeethSocket(_2065.GearTeethSocket):
    """ConceptGearTeethSocket

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_TEETH_SOCKET

    def __init__(self, instance_to_wrap: 'ConceptGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
