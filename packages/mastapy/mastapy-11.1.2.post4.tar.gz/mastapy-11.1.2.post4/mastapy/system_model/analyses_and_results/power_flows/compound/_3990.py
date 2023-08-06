"""_3990.py

PlanetaryConnectionCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.connections_and_sockets import _2038
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3858
from mastapy.system_model.analyses_and_results.power_flows.compound import _4004
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PlanetaryConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundPowerFlow',)


class PlanetaryConnectionCompoundPowerFlow(_4004.ShaftToMountableComponentConnectionCompoundPowerFlow):
    """PlanetaryConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _PLANETARY_CONNECTION_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2038.PlanetaryConnection':
        """PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2038.PlanetaryConnection':
        """PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3858.PlanetaryConnectionPowerFlow]':
        """List[PlanetaryConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3858.PlanetaryConnectionPowerFlow]':
        """List[PlanetaryConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
