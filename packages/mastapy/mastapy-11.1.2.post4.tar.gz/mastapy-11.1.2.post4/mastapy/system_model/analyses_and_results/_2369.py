"""_2369.py

SingleAnalysis
"""


from mastapy._internal import constructor
from mastapy import _7285, _7279
from mastapy.system_model import _1960
from mastapy.system_model.analyses_and_results import _2400
from mastapy._internal.python_net import python_net_import

_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_DESIGN_ENTITY = python_net_import('SMT.MastaAPI.SystemModel', 'DesignEntity')
_DESIGN_ENTITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DesignEntityAnalysis')
_SINGLE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'SingleAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleAnalysis',)


class SingleAnalysis(_7279.MarshalByRefObjectPermanent):
    """SingleAnalysis

    This is a mastapy class.
    """

    TYPE = _SINGLE_ANALYSIS

    def __init__(self, instance_to_wrap: 'SingleAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def results_ready(self) -> 'bool':
        """bool: 'ResultsReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultsReady

        if temp is None:
            return None

        return temp

    def perform_analysis(self):
        """ 'PerformAnalysis' is the original name of this method."""

        self.wrapped.PerformAnalysis()

    def perform_analysis_with_progress(self, task_progress: '_7285.TaskProgress'):
        """ 'PerformAnalysis' is the original name of this method.

        Args:
            task_progress (mastapy.TaskProgress)
        """

        self.wrapped.PerformAnalysis.Overloads[_TASK_PROGRESS](task_progress.wrapped if task_progress else None)

    def results_for(self, design_entity: '_1960.DesignEntity') -> '_2400.DesignEntityAnalysis':
        """ 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)

        Returns:
            mastapy.system_model.analyses_and_results.DesignEntityAnalysis
        """

        method_result = self.wrapped.ResultsFor.Overloads[_DESIGN_ENTITY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def results_for_design_entity_analysis(self, design_entity_analysis: '_2400.DesignEntityAnalysis') -> '_2400.DesignEntityAnalysis':
        """ 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.DesignEntityAnalysis)

        Returns:
            mastapy.system_model.analyses_and_results.DesignEntityAnalysis
        """

        method_result = self.wrapped.ResultsFor.Overloads[_DESIGN_ENTITY_ANALYSIS](design_entity_analysis.wrapped if design_entity_analysis else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
