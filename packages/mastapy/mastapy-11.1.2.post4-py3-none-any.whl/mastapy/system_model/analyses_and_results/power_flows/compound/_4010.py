"""_4010.py

SpringDamperConnectionCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2101
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3879
from mastapy.system_model.analyses_and_results.power_flows.compound import _3945
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SpringDamperConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionCompoundPowerFlow',)


class SpringDamperConnectionCompoundPowerFlow(_3945.CouplingConnectionCompoundPowerFlow):
    """SpringDamperConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_CONNECTION_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2101.SpringDamperConnection':
        """SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2101.SpringDamperConnection':
        """SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3879.SpringDamperConnectionPowerFlow]':
        """List[SpringDamperConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3879.SpringDamperConnectionPowerFlow]':
        """List[SpringDamperConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
