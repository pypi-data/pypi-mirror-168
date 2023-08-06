"""_1038.py

StandardRackFlank
"""


from mastapy.gears.gear_designs.cylindrical import _972
from mastapy._internal.python_net import python_net_import

_STANDARD_RACK_FLANK = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'StandardRackFlank')


__docformat__ = 'restructuredtext en'
__all__ = ('StandardRackFlank',)


class StandardRackFlank(_972.CylindricalGearBasicRackFlank):
    """StandardRackFlank

    This is a mastapy class.
    """

    TYPE = _STANDARD_RACK_FLANK

    def __init__(self, instance_to_wrap: 'StandardRackFlank.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
