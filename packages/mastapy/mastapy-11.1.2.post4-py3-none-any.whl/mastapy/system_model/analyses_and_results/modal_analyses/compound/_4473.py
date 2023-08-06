"""_4473.py

BearingCompoundModalAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2191
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4320
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4501
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BearingCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundModalAnalysis',)


class BearingCompoundModalAnalysis(_4501.ConnectorCompoundModalAnalysis):
    """BearingCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE = _BEARING_COMPOUND_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'BearingCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2191.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4320.BearingModalAnalysis]':
        """List[BearingModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundModalAnalysis]':
        """List[BearingCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4320.BearingModalAnalysis]':
        """List[BearingModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
