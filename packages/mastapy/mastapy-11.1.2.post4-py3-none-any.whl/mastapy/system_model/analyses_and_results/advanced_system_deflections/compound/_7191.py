"""_7191.py

GearMeshCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7060
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7197
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GearMeshCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundAdvancedSystemDeflection',)


class GearMeshCompoundAdvancedSystemDeflection(_7197.InterMountableComponentConnectionCompoundAdvancedSystemDeflection):
    """GearMeshCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'GearMeshCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_separation_left_flank(self) -> 'float':
        """float: 'MinimumSeparationLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumSeparationLeftFlank

        if temp is None:
            return None

        return temp

    @property
    def minimum_separation_right_flank(self) -> 'float':
        """float: 'MinimumSeparationRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumSeparationRightFlank

        if temp is None:
            return None

        return temp

    @property
    def connection_analysis_cases(self) -> 'List[_7060.GearMeshAdvancedSystemDeflection]':
        """List[GearMeshAdvancedSystemDeflection]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_7060.GearMeshAdvancedSystemDeflection]':
        """List[GearMeshAdvancedSystemDeflection]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
