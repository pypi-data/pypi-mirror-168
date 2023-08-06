"""_918.py

ZerolBevelMeshedGearDesign
"""


from mastapy.gears.gear_designs.bevel import _1137
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.ZerolBevel', 'ZerolBevelMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelMeshedGearDesign',)


class ZerolBevelMeshedGearDesign(_1137.BevelMeshedGearDesign):
    """ZerolBevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'ZerolBevelMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
