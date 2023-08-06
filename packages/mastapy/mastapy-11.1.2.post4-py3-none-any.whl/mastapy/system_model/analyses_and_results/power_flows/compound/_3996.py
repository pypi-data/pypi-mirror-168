"""_3996.py

RingPinsCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.cycloidal import _2319
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3866
from mastapy.system_model.analyses_and_results.power_flows.compound import _3984
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RingPinsCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundPowerFlow',)


class RingPinsCompoundPowerFlow(_3984.MountableComponentCompoundPowerFlow):
    """RingPinsCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _RING_PINS_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'RingPinsCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2319.RingPins':
        """RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3866.RingPinsPowerFlow]':
        """List[RingPinsPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3866.RingPinsPowerFlow]':
        """List[RingPinsPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
