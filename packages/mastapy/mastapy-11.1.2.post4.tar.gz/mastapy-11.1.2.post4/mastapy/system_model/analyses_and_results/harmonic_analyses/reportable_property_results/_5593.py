"""_5593.py

ResultsForMultipleOrdersForFESurface
"""


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5590, _5592
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_MULTIPLE_ORDERS_FOR_FE_SURFACE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'ResultsForMultipleOrdersForFESurface')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForMultipleOrdersForFESurface',)


class ResultsForMultipleOrdersForFESurface(_5592.ResultsForMultipleOrders):
    """ResultsForMultipleOrdersForFESurface

    This is a mastapy class.
    """

    TYPE = _RESULTS_FOR_MULTIPLE_ORDERS_FOR_FE_SURFACE

    def __init__(self, instance_to_wrap: 'ResultsForMultipleOrdersForFESurface.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_surfaces(self) -> 'List[_5590.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic]':
        """List[HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic]: 'FESurfaces' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FESurfaces

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
