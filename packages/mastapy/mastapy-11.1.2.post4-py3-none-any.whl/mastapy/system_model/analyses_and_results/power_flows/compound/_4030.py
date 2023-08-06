"""_4030.py

WormGearCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.gears import _2300
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _344
from mastapy.system_model.analyses_and_results.power_flows import _3902
from mastapy.system_model.analyses_and_results.power_flows.compound import _3965
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'WormGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundPowerFlow',)


class WormGearCompoundPowerFlow(_3965.GearCompoundPowerFlow):
    """WormGearCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'WormGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2300.WormGear':
        """WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating(self) -> '_344.WormGearDutyCycleRating':
        """WormGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_duty_cycle_rating(self) -> '_344.WormGearDutyCycleRating':
        """WormGearDutyCycleRating: 'WormGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearDutyCycleRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3902.WormGearPowerFlow]':
        """List[WormGearPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3902.WormGearPowerFlow]':
        """List[WormGearPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
