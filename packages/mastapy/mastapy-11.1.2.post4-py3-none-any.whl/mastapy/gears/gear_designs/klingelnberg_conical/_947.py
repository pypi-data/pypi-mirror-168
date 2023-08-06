"""_947.py

KlingelnbergConicalMeshedGearDesign
"""


from mastapy.gears.gear_designs.conical import _1113
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CONICAL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergConical', 'KlingelnbergConicalMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalMeshedGearDesign',)


class KlingelnbergConicalMeshedGearDesign(_1113.ConicalMeshedGearDesign):
    """KlingelnbergConicalMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CONICAL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
