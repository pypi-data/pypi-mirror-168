"""_5515.py

OilSealHarmonicAnalysis
"""


from mastapy.system_model.part_model import _2216
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6653
from mastapy.system_model.analyses_and_results.system_deflections import _2528
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5450
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'OilSealHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealHarmonicAnalysis',)


class OilSealHarmonicAnalysis(_5450.ConnectorHarmonicAnalysis):
    """OilSealHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'OilSealHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2216.OilSeal':
        """OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6653.OilSealLoadCase':
        """OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2528.OilSealSystemDeflection':
        """OilSealSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
