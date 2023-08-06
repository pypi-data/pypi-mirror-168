"""_7026.py

ConceptCouplingConnectionAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2095
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6561
from mastapy.system_model.analyses_and_results.system_deflections import _2461
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7038
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ConceptCouplingConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionAdvancedSystemDeflection',)


class ConceptCouplingConnectionAdvancedSystemDeflection(_7038.CouplingConnectionAdvancedSystemDeflection):
    """ConceptCouplingConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2095.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6561.ConceptCouplingConnectionLoadCase':
        """ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2461.ConceptCouplingConnectionSystemDeflection]':
        """List[ConceptCouplingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
