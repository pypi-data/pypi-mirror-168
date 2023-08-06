"""_6024.py

ClutchDynamicAnalysis
"""


from mastapy.system_model.part_model.couplings import _2327
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6558
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6040
from mastapy._internal.python_net import python_net_import

_CLUTCH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ClutchDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchDynamicAnalysis',)


class ClutchDynamicAnalysis(_6040.CouplingDynamicAnalysis):
    """ClutchDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2327.Clutch':
        """Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6558.ClutchLoadCase':
        """ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
