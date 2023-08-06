"""_2300.py

WormGear
"""


from mastapy.gears.gear_designs.worm import _920, _919, _923
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import _2279
from mastapy._internal.python_net import python_net_import

_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGear',)


class WormGear(_2279.Gear):
    """WormGear

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR

    def __init__(self, instance_to_wrap: 'WormGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_design(self) -> '_920.WormGearDesign':
        """WormGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearDesign

        if temp is None:
            return None

        if _920.WormGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to WormGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_design(self) -> '_920.WormGearDesign':
        """WormGearDesign: 'WormGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearDesign

        if temp is None:
            return None

        if _920.WormGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast worm_gear_design to WormGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
