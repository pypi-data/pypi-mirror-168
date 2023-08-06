"""_3551.py

CycloidalAssemblyStabilityAnalysis
"""


from mastapy.system_model.part_model.cycloidal import _2317
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6580
from mastapy.system_model.analyses_and_results.stability_analyses import _3606
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CycloidalAssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyStabilityAnalysis',)


class CycloidalAssemblyStabilityAnalysis(_3606.SpecialisedAssemblyStabilityAnalysis):
    """CycloidalAssemblyStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_ASSEMBLY_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2317.CycloidalAssembly':
        """CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6580.CycloidalAssemblyLoadCase':
        """CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
