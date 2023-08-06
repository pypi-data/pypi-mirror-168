"""_3565.py

FlexiblePinAssemblyStabilityAnalysis
"""


from mastapy.system_model.part_model import _2204
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6612
from mastapy.system_model.analyses_and_results.stability_analyses import _3606
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'FlexiblePinAssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyStabilityAnalysis',)


class FlexiblePinAssemblyStabilityAnalysis(_3606.SpecialisedAssemblyStabilityAnalysis):
    """FlexiblePinAssemblyStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2204.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6612.FlexiblePinAssemblyLoadCase':
        """FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
