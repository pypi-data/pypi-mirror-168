"""_5513.py

MeasurementComponentHarmonicAnalysis
"""


from mastapy.system_model.part_model import _2213
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6648
from mastapy.system_model.analyses_and_results.system_deflections import _2524
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5563
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'MeasurementComponentHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentHarmonicAnalysis',)


class MeasurementComponentHarmonicAnalysis(_5563.VirtualComponentHarmonicAnalysis):
    """MeasurementComponentHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _MEASUREMENT_COMPONENT_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'MeasurementComponentHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6648.MeasurementComponentLoadCase':
        """MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2524.MeasurementComponentSystemDeflection':
        """MeasurementComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
