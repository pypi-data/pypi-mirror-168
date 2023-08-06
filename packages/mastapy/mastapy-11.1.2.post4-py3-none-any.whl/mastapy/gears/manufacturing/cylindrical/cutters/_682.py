"""_682.py

CylindricalGearShaverDatabase
"""


from mastapy.gears.manufacturing.cylindrical import _576
from mastapy.gears.manufacturing.cylindrical.cutters import _681
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SHAVER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearShaverDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearShaverDatabase',)


class CylindricalGearShaverDatabase(_576.CylindricalCutterDatabase['_681.CylindricalGearShaver']):
    """CylindricalGearShaverDatabase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SHAVER_DATABASE

    def __init__(self, instance_to_wrap: 'CylindricalGearShaverDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
