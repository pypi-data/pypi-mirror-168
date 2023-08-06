"""_2648.py

ExternalCADModelCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2202
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2496
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2620
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ExternalCADModelCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundSystemDeflection',)


class ExternalCADModelCompoundSystemDeflection(_2620.ComponentCompoundSystemDeflection):
    """ExternalCADModelCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2496.ExternalCADModelSystemDeflection]':
        """List[ExternalCADModelSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2496.ExternalCADModelSystemDeflection]':
        """List[ExternalCADModelSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
