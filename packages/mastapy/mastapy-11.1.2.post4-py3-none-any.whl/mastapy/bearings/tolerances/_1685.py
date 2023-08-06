"""_1685.py

SupportMaterialSource
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SUPPORT_MATERIAL_SOURCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'SupportMaterialSource')


__docformat__ = 'restructuredtext en'
__all__ = ('SupportMaterialSource',)


class SupportMaterialSource(Enum):
    """SupportMaterialSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _SUPPORT_MATERIAL_SOURCE

    SHAFT = 0
    DESIGN_HOUSING = 1
    FE_COMPONENT = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


SupportMaterialSource.__setattr__ = __enum_setattr
SupportMaterialSource.__delattr__ = __enum_delattr
