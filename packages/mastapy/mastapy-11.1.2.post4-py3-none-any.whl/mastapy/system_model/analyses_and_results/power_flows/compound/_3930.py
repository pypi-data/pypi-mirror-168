"""_3930.py

ClutchHalfCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2328
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3796
from mastapy.system_model.analyses_and_results.power_flows.compound import _3946
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ClutchHalfCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundPowerFlow',)


class ClutchHalfCompoundPowerFlow(_3946.CouplingHalfCompoundPowerFlow):
    """ClutchHalfCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3796.ClutchHalfPowerFlow]':
        """List[ClutchHalfPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3796.ClutchHalfPowerFlow]':
        """List[ClutchHalfPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
