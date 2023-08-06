"""_4305.py

VirtualComponentCompoundParametricStudyTool
"""


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import _4176
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4260
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'VirtualComponentCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundParametricStudyTool',)


class VirtualComponentCompoundParametricStudyTool(_4260.MountableComponentCompoundParametricStudyTool):
    """VirtualComponentCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_4176.VirtualComponentParametricStudyTool]':
        """List[VirtualComponentParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4176.VirtualComponentParametricStudyTool]':
        """List[VirtualComponentParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
