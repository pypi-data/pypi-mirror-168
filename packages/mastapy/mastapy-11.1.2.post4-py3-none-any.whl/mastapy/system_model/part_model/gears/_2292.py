"""_2292.py

SpiralBevelGear
"""


from mastapy.gears.gear_designs.spiral_bevel import _932
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2268
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGear',)


class SpiralBevelGear(_2268.BevelGear):
    """SpiralBevelGear

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR

    def __init__(self, instance_to_wrap: 'SpiralBevelGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_design(self) -> '_932.SpiralBevelGearDesign':
        """SpiralBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def spiral_bevel_gear_design(self) -> '_932.SpiralBevelGearDesign':
        """SpiralBevelGearDesign: 'SpiralBevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
