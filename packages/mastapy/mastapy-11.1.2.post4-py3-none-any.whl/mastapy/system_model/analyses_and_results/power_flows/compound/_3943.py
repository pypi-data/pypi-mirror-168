"""_3943.py

ConnectorCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.analyses_and_results.power_flows import _3810
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3984
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConnectorCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundPowerFlow',)


class ConnectorCompoundPowerFlow(_3984.MountableComponentCompoundPowerFlow):
    """ConnectorCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ConnectorCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_3810.ConnectorPowerFlow]':
        """List[ConnectorPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_3810.ConnectorPowerFlow]':
        """List[ConnectorPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
