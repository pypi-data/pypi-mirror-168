"""_2640.py

CycloidalDiscCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.cycloidal import _2318
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2482
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2596
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CycloidalDiscCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundSystemDeflection',)


class CycloidalDiscCompoundSystemDeflection(_2596.AbstractShaftCompoundSystemDeflection):
    """CycloidalDiscCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2482.CycloidalDiscSystemDeflection]':
        """List[CycloidalDiscSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2482.CycloidalDiscSystemDeflection]':
        """List[CycloidalDiscSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
