"""_2422.py

CompoundModalAnalysisAtAStiffness
"""


from mastapy.system_model.analyses_and_results import _2368
from mastapy._internal.python_net import python_net_import

_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysisAtAStiffness',)


class CompoundModalAnalysisAtAStiffness(_2368.CompoundAnalysis):
    """CompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
