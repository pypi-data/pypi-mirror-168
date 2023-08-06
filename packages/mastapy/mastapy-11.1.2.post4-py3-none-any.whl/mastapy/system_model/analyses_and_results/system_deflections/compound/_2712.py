"""_2712.py

SynchroniserPartCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2566
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2634
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PART_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SynchroniserPartCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPartCompoundSystemDeflection',)


class SynchroniserPartCompoundSystemDeflection(_2634.CouplingHalfCompoundSystemDeflection):
    """SynchroniserPartCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_PART_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'SynchroniserPartCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_2566.SynchroniserPartSystemDeflection]':
        """List[SynchroniserPartSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_2566.SynchroniserPartSystemDeflection]':
        """List[SynchroniserPartSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
