"""_2384.py

ModalAnalysis
"""


from mastapy.system_model.analyses_and_results.modal_analyses import _4393, _4391, _2378
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _2375
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2779
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _2379
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4646
from mastapy.system_model.analyses_and_results.harmonic_analyses import _2377
from mastapy.system_model.analyses_and_results.analysis_cases import _7276
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysis',)


class ModalAnalysis(_7276.StaticLoadAnalysisCase):
    """ModalAnalysis

    This is a mastapy class.
    """

    TYPE = _MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'ModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_settings(self) -> '_4393.ModalAnalysisOptions':
        """ModalAnalysisOptions: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bar_model_export(self) -> '_4391.ModalAnalysisBarModelFEExportOptions':
        """ModalAnalysisBarModelFEExportOptions: 'BarModelExport' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BarModelExport

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def modal_analysis_results(self) -> '_2375.DynamicAnalysis':
        """DynamicAnalysis: 'ModalAnalysisResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModalAnalysisResults

        if temp is None:
            return None

        if _2375.DynamicAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast modal_analysis_results to DynamicAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
