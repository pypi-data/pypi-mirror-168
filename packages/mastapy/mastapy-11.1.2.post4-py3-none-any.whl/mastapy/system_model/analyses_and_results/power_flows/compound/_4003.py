"""_4003.py

ShaftHubConnectionCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2347
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3872
from mastapy.system_model.analyses_and_results.power_flows.compound import _3943
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ShaftHubConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundPowerFlow',)


class ShaftHubConnectionCompoundPowerFlow(_3943.ConnectorCompoundPowerFlow):
    """ShaftHubConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3872.ShaftHubConnectionPowerFlow]':
        """List[ShaftHubConnectionPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3872.ShaftHubConnectionPowerFlow]':
        """List[ShaftHubConnectionPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
