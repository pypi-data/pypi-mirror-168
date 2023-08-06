"""_939.py

KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
"""


from mastapy.gears.gear_designs.klingelnberg_conical import _947
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergSpiralBevel', 'KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign',)


class KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign(_947.KlingelnbergConicalMeshedGearDesign):
    """KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
