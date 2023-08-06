"""_3991.py

PlanetaryGearSetCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.analyses_and_results.power_flows import _3859
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3956
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PlanetaryGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetCompoundPowerFlow',)


class PlanetaryGearSetCompoundPowerFlow(_3956.CylindricalGearSetCompoundPowerFlow):
    """PlanetaryGearSetCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _PLANETARY_GEAR_SET_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3859.PlanetaryGearSetPowerFlow]':
        """List[PlanetaryGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3859.PlanetaryGearSetPowerFlow]':
        """List[PlanetaryGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
