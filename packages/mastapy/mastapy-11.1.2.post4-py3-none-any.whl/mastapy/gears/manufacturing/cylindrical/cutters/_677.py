"""_677.py

CylindricalGearPlungeShaverDatabase
"""


from mastapy.gears.manufacturing.cylindrical import _576
from mastapy.gears.manufacturing.cylindrical.cutters import _676
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PLUNGE_SHAVER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearPlungeShaverDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearPlungeShaverDatabase',)


class CylindricalGearPlungeShaverDatabase(_576.CylindricalCutterDatabase['_676.CylindricalGearPlungeShaver']):
    """CylindricalGearPlungeShaverDatabase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_PLUNGE_SHAVER_DATABASE

    def __init__(self, instance_to_wrap: 'CylindricalGearPlungeShaverDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
