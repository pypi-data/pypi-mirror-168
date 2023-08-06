"""_5444.py

ConceptGearMeshHarmonicAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2056
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6565
from mastapy.system_model.analyses_and_results.system_deflections import _2464
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5487
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ConceptGearMeshHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshHarmonicAnalysis',)


class ConceptGearMeshHarmonicAnalysis(_5487.GearMeshHarmonicAnalysis):
    """ConceptGearMeshHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptGearMeshHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2056.ConceptGearMesh':
        """ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6565.ConceptGearMeshLoadCase':
        """ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2464.ConceptGearMeshSystemDeflection':
        """ConceptGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
