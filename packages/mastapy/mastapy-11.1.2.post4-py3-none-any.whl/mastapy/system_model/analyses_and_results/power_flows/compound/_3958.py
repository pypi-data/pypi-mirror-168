"""_3958.py

DatumCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3826
from mastapy.system_model.analyses_and_results.power_flows.compound import _3932
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'DatumCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundPowerFlow',)


class DatumCompoundPowerFlow(_3932.ComponentCompoundPowerFlow):
    """DatumCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _DATUM_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'DatumCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.Datum':
        """Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3826.DatumPowerFlow]':
        """List[DatumPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3826.DatumPowerFlow]':
        """List[DatumPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
