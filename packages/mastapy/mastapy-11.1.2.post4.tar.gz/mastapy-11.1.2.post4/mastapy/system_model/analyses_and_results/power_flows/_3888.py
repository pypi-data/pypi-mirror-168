"""_3888.py

StraightBevelPlanetGearPowerFlow
"""


from mastapy.system_model.part_model.gears import _2298
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3883
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelPlanetGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearPowerFlow',)


class StraightBevelPlanetGearPowerFlow(_3883.StraightBevelDiffGearPowerFlow):
    """StraightBevelPlanetGearPowerFlow

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_POWER_FLOW

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2298.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
