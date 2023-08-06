"""_5594.py

ResultsForMultipleOrdersForGroups
"""


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5587, _5592
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_MULTIPLE_ORDERS_FOR_GROUPS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'ResultsForMultipleOrdersForGroups')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForMultipleOrdersForGroups',)


class ResultsForMultipleOrdersForGroups(_5592.ResultsForMultipleOrders):
    """ResultsForMultipleOrdersForGroups

    This is a mastapy class.
    """

    TYPE = _RESULTS_FOR_MULTIPLE_ORDERS_FOR_GROUPS

    def __init__(self, instance_to_wrap: 'ResultsForMultipleOrdersForGroups.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def groups(self) -> 'List[_5587.HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic]':
        """List[HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic]: 'Groups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Groups

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
