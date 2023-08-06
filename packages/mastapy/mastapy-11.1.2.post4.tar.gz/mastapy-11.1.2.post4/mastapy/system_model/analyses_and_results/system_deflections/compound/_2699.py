"""_2699.py

SpringDamperCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2349
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2556
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2632
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SpringDamperCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundSystemDeflection',)


class SpringDamperCompoundSystemDeflection(_2632.CouplingCompoundSystemDeflection):
    """SpringDamperCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2349.SpringDamper':
        """SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2349.SpringDamper':
        """SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2556.SpringDamperSystemDeflection]':
        """List[SpringDamperSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2556.SpringDamperSystemDeflection]':
        """List[SpringDamperSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
