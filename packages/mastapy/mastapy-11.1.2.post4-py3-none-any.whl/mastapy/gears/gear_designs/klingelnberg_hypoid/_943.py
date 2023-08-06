"""_943.py

KlingelnbergCycloPalloidHypoidMeshedGearDesign
"""


from mastapy.gears.gear_designs.klingelnberg_conical import _947
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergHypoid', 'KlingelnbergCycloPalloidHypoidMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidMeshedGearDesign',)


class KlingelnbergCycloPalloidHypoidMeshedGearDesign(_947.KlingelnbergConicalMeshedGearDesign):
    """KlingelnbergCycloPalloidHypoidMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
