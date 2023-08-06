"""_5542.py

SpringDamperConnectionHarmonicAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2101
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6684
from mastapy.system_model.analyses_and_results.system_deflections import _2554
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5451
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SpringDamperConnectionHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionHarmonicAnalysis',)


class SpringDamperConnectionHarmonicAnalysis(_5451.CouplingConnectionHarmonicAnalysis):
    """SpringDamperConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_CONNECTION_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2101.SpringDamperConnection':
        """SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6684.SpringDamperConnectionLoadCase':
        """SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2554.SpringDamperConnectionSystemDeflection':
        """SpringDamperConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
