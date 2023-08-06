"""_2637.py

CVTPulleyCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2477
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2684
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CVTPulleyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundSystemDeflection',)


class CVTPulleyCompoundSystemDeflection(_2684.PulleyCompoundSystemDeflection):
    """CVTPulleyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_2477.CVTPulleySystemDeflection]':
        """List[CVTPulleySystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2477.CVTPulleySystemDeflection]':
        """List[CVTPulleySystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
