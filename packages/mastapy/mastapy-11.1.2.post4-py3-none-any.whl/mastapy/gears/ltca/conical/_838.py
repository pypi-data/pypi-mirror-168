"""_838.py

ConicalMeshLoadedContactLine
"""


from mastapy.gears.ltca import _809
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_LOADED_CONTACT_LINE = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalMeshLoadedContactLine')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshLoadedContactLine',)


class ConicalMeshLoadedContactLine(_809.GearMeshLoadedContactLine):
    """ConicalMeshLoadedContactLine

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_LOADED_CONTACT_LINE

    def __init__(self, instance_to_wrap: 'ConicalMeshLoadedContactLine.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
