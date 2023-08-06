"""_3584.py

MeasurementComponentStabilityAnalysis
"""


from mastapy.system_model.part_model import _2213
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6648
from mastapy.system_model.analyses_and_results.stability_analyses import _3632
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'MeasurementComponentStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentStabilityAnalysis',)


class MeasurementComponentStabilityAnalysis(_3632.VirtualComponentStabilityAnalysis):
    """MeasurementComponentStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _MEASUREMENT_COMPONENT_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'MeasurementComponentStabilityAnalysis.TYPE'):
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
