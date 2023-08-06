"""_4588.py

WormGearCompoundModalAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2300
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4448
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4523
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'WormGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundModalAnalysis',)


class WormGearCompoundModalAnalysis(_4523.GearCompoundModalAnalysis):
    """WormGearCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_COMPOUND_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'WormGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2300.WormGear':
        """WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4448.WormGearModalAnalysis]':
        """List[WormGearModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4448.WormGearModalAnalysis]':
        """List[WormGearModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
