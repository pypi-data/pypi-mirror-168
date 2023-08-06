"""_933.py

SpiralBevelGearMeshDesign
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.spiral_bevel import _934, _932, _935
from mastapy.gears.gear_designs.bevel import _1135
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.SpiralBevel', 'SpiralBevelGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshDesign',)


class SpiralBevelGearMeshDesign(_1135.BevelGearMeshDesign):
    """SpiralBevelGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wheel_inner_blade_angle_convex(self) -> 'float':
        """float: 'WheelInnerBladeAngleConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInnerBladeAngleConvex

        if temp is None:
            return None

        return temp

    @property
    def wheel_outer_blade_angle_concave(self) -> 'float':
        """float: 'WheelOuterBladeAngleConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelOuterBladeAngleConcave

        if temp is None:
            return None

        return temp

    @property
    def spiral_bevel_gear_set(self) -> '_934.SpiralBevelGearSetDesign':
        """SpiralBevelGearSetDesign: 'SpiralBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def spiral_bevel_gears(self) -> 'List[_932.SpiralBevelGearDesign]':
        """List[SpiralBevelGearDesign]: 'SpiralBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_meshed_gears(self) -> 'List[_935.SpiralBevelMeshedGearDesign]':
        """List[SpiralBevelMeshedGearDesign]: 'SpiralBevelMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelMeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
