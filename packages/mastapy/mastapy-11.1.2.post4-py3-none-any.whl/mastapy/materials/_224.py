"""_224.py

BearingMaterialDatabase
"""


from mastapy.utility.databases import _1604
from mastapy.materials import _223
from mastapy._internal.python_net import python_net_import

_BEARING_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'BearingMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMaterialDatabase',)


class BearingMaterialDatabase(_1604.NamedDatabase['_223.BearingMaterial']):
    """BearingMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _BEARING_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'BearingMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
