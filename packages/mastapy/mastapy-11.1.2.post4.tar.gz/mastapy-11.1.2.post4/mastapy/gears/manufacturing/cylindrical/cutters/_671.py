"""_671.py

CylindricalFormedWheelGrinderDatabase
"""


from mastapy.gears.manufacturing.cylindrical import _576
from mastapy.gears.manufacturing.cylindrical.cutters import _673
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_FORMED_WHEEL_GRINDER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalFormedWheelGrinderDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalFormedWheelGrinderDatabase',)


class CylindricalFormedWheelGrinderDatabase(_576.CylindricalCutterDatabase['_673.CylindricalGearFormGrindingWheel']):
    """CylindricalFormedWheelGrinderDatabase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_FORMED_WHEEL_GRINDER_DATABASE

    def __init__(self, instance_to_wrap: 'CylindricalFormedWheelGrinderDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
