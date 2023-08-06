"""_937.py

KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
"""


from typing import List

from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _938, _936, _939
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.klingelnberg_conical import _945
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergSpiralBevel', 'KlingelnbergCycloPalloidSpiralBevelGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshDesign',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshDesign(_945.KlingelnbergConicalGearMeshDesign):
    """KlingelnbergCycloPalloidSpiralBevelGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_938.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        """KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'KlingelnbergCycloPalloidSpiralBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears(self) -> 'List[_936.KlingelnbergCycloPalloidSpiralBevelGearDesign]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearDesign]: 'KlingelnbergCycloPalloidSpiralBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshed_gears(self) -> 'List[_939.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign]':
        """List[KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign]: 'KlingelnbergCycloPalloidSpiralBevelMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
