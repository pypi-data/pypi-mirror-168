"""_972.py

CylindricalGearBasicRackFlank
"""


from mastapy.gears.gear_designs.cylindrical import _970
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_BASIC_RACK_FLANK = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearBasicRackFlank')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearBasicRackFlank',)


class CylindricalGearBasicRackFlank(_970.CylindricalGearAbstractRackFlank):
    """CylindricalGearBasicRackFlank

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_BASIC_RACK_FLANK

    def __init__(self, instance_to_wrap: 'CylindricalGearBasicRackFlank.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
