"""_57.py

FEMeshingOperation
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FE_MESHING_OPERATION = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEMeshingOperation')


__docformat__ = 'restructuredtext en'
__all__ = ('FEMeshingOperation',)


class FEMeshingOperation(Enum):
    """FEMeshingOperation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _FE_MESHING_OPERATION

    MESHSURFACE = 0
    MESHVOLUME = 1
    MESHCROSSSECTION = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


FEMeshingOperation.__setattr__ = __enum_setattr
FEMeshingOperation.__delattr__ = __enum_delattr
