"""_3910.py

AbstractShaftToMountableComponentConnectionCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.analyses_and_results.power_flows import _3777
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3942
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AbstractShaftToMountableComponentConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnectionCompoundPowerFlow',)


class AbstractShaftToMountableComponentConnectionCompoundPowerFlow(_3942.ConnectionCompoundPowerFlow):
    """AbstractShaftToMountableComponentConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_3777.AbstractShaftToMountableComponentConnectionPowerFlow]':
        """List[AbstractShaftToMountableComponentConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3777.AbstractShaftToMountableComponentConnectionPowerFlow]':
        """List[AbstractShaftToMountableComponentConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
