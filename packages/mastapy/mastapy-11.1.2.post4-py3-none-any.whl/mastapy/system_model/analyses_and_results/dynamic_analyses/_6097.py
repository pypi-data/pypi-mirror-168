"""_6097.py

RootAssemblyDynamicAnalysis
"""


from mastapy.system_model.part_model import _2224
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _2375, _6009
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2779
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _2379
from mastapy.system_model.analyses_and_results.modal_analyses import _2378
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4646
from mastapy.system_model.analyses_and_results.harmonic_analyses import _2377
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RootAssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyDynamicAnalysis',)


class RootAssemblyDynamicAnalysis(_6009.AssemblyDynamicAnalysis):
    """RootAssemblyDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'RootAssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2224.RootAssembly':
        """RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_analysis_inputs(self) -> '_2375.DynamicAnalysis':
        """DynamicAnalysis: 'DynamicAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAnalysisInputs

        if temp is None:
            return None

        if _2375.DynamicAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_inputs to DynamicAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
