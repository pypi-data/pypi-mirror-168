"""_2368.py

CompoundAnalysis
"""


from typing import Iterable

from mastapy._internal import constructor, conversion
from mastapy import _7285, _7279
from mastapy.system_model import _1960
from mastapy.system_model.analyses_and_results.analysis_cases import _7269
from mastapy._internal.python_net import python_net_import

_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_COMPOUND_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundAnalysis',)


class CompoundAnalysis(_7279.MarshalByRefObjectPermanent):
    """CompoundAnalysis

    This is a mastapy class.
    """

    TYPE = _COMPOUND_ANALYSIS

    def __init__(self, instance_to_wrap: 'CompoundAnalysis.TYPE'):
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

    def perform_analysis_with_progress(self, progress: '_7285.TaskProgress'):
        """ 'PerformAnalysis' is the original name of this method.

        Args:
            progress (mastapy.TaskProgress)
        """

        self.wrapped.PerformAnalysis.Overloads[_TASK_PROGRESS](progress.wrapped if progress else None)

    def results_for(self, design_entity: '_1960.DesignEntity') -> 'Iterable[_7269.DesignEntityCompoundAnalysis]':
        """ 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.DesignEntity)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.analysis_cases.DesignEntityCompoundAnalysis]
        """

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None))
