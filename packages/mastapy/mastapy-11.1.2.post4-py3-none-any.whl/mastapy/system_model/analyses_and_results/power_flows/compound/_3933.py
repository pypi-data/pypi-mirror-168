"""_3933.py

ConceptCouplingCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2330
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3802
from mastapy.system_model.analyses_and_results.power_flows.compound import _3944
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConceptCouplingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundPowerFlow',)


class ConceptCouplingCompoundPowerFlow(_3944.CouplingCompoundPowerFlow):
    """ConceptCouplingCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2330.ConceptCoupling':
        """ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2330.ConceptCoupling':
        """ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3802.ConceptCouplingPowerFlow]':
        """List[ConceptCouplingPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3802.ConceptCouplingPowerFlow]':
        """List[ConceptCouplingPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
