"""_2652.py

FEPartCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2501
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2597
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'FEPartCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundSystemDeflection',)


class FEPartCompoundSystemDeflection(_2597.AbstractShaftOrHousingCompoundSystemDeflection):
    """FEPartCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _FE_PART_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'FEPartCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2501.FEPartSystemDeflection]':
        """List[FEPartSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundSystemDeflection]':
        """List[FEPartCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2501.FEPartSystemDeflection]':
        """List[FEPartSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
