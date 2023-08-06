"""_3889.py

StraightBevelSunGearPowerFlow
"""


from mastapy.system_model.part_model.gears import _2299
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3883
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelSunGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearPowerFlow',)


class StraightBevelSunGearPowerFlow(_3883.StraightBevelDiffGearPowerFlow):
    """StraightBevelSunGearPowerFlow

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_POWER_FLOW

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
