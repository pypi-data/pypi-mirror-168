"""_2646.py

DatumCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2495
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2620
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'DatumCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundSystemDeflection',)


class DatumCompoundSystemDeflection(_2620.ComponentCompoundSystemDeflection):
    """DatumCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _DATUM_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'DatumCompoundSystemDeflection.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_2495.DatumSystemDeflection]':
        """List[DatumSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2495.DatumSystemDeflection]':
        """List[DatumSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
