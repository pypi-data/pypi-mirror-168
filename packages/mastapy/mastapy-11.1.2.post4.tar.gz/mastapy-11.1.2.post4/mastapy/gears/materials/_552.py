"""_552.py

BevelGearIsoMaterialDatabase
"""


from mastapy.gears.materials import _550, _551
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_ISO_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'BevelGearIsoMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearIsoMaterialDatabase',)


class BevelGearIsoMaterialDatabase(_550.BevelGearAbstractMaterialDatabase['_551.BevelGearISOMaterial']):
    """BevelGearIsoMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_ISO_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'BevelGearIsoMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
