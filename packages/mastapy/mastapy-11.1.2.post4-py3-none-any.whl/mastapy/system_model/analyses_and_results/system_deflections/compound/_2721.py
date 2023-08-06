"""_2721.py

WormGearMeshCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2080
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2580
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2655
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'WormGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundSystemDeflection',)


class WormGearMeshCompoundSystemDeflection(_2655.GearMeshCompoundSystemDeflection):
    """WormGearMeshCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2080.WormGearMesh':
        """WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2080.WormGearMesh':
        """WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_2580.WormGearMeshSystemDeflection]':
        """List[WormGearMeshSystemDeflection]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_2580.WormGearMeshSystemDeflection]':
        """List[WormGearMeshSystemDeflection]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
