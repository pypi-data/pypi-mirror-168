"""_4020.py

SynchroniserCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2351
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3892
from mastapy.system_model.analyses_and_results.power_flows.compound import _4005
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SynchroniserCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundPowerFlow',)


class SynchroniserCompoundPowerFlow(_4005.SpecialisedAssemblyCompoundPowerFlow):
    """SynchroniserCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2351.Synchroniser':
        """Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2351.Synchroniser':
        """Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3892.SynchroniserPowerFlow]':
        """List[SynchroniserPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3892.SynchroniserPowerFlow]':
        """List[SynchroniserPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
