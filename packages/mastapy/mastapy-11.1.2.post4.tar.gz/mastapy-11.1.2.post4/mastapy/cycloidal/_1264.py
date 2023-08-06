"""_1264.py

CycloidalDiscMaterialDatabase
"""


from mastapy.materials import _246
from mastapy.cycloidal import _1263
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscMaterialDatabase',)


class CycloidalDiscMaterialDatabase(_246.MaterialDatabase['_1263.CycloidalDiscMaterial']):
    """CycloidalDiscMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'CycloidalDiscMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
