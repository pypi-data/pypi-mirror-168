"""_2631.py

ConnectorCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2472
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2673
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConnectorCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundSystemDeflection',)


class ConnectorCompoundSystemDeflection(_2673.MountableComponentCompoundSystemDeflection):
    """ConnectorCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ConnectorCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_2472.ConnectorSystemDeflection]':
        """List[ConnectorSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_2472.ConnectorSystemDeflection]':
        """List[ConnectorSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
