"""_951.py

HypoidMeshedGearDesign
"""


from mastapy.gears.gear_designs.agma_gleason_conical import _1150
from mastapy._internal.python_net import python_net_import

_HYPOID_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Hypoid', 'HypoidMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidMeshedGearDesign',)


class HypoidMeshedGearDesign(_1150.AGMAGleasonConicalMeshedGearDesign):
    """HypoidMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _HYPOID_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'HypoidMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
