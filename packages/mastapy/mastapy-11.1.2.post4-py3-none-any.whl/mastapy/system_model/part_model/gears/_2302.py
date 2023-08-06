"""_2302.py

ZerolBevelGear
"""


from mastapy.gears.gear_designs.zerol_bevel import _915
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2268
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGear',)


class ZerolBevelGear(_2268.BevelGear):
    """ZerolBevelGear

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR

    def __init__(self, instance_to_wrap: 'ZerolBevelGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_design(self) -> '_915.ZerolBevelGearDesign':
        """ZerolBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def zerol_bevel_gear_design(self) -> '_915.ZerolBevelGearDesign':
        """ZerolBevelGearDesign: 'ZerolBevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
