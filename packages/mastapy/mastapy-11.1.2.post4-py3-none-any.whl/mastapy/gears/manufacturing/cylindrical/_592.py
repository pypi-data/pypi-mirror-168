"""_592.py

CylindricalShaperDatabase
"""


from mastapy.gears.manufacturing.cylindrical import _576
from mastapy.gears.manufacturing.cylindrical.cutters import _680
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_SHAPER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalShaperDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalShaperDatabase',)


class CylindricalShaperDatabase(_576.CylindricalCutterDatabase['_680.CylindricalGearShaper']):
    """CylindricalShaperDatabase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_SHAPER_DATABASE

    def __init__(self, instance_to_wrap: 'CylindricalShaperDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
