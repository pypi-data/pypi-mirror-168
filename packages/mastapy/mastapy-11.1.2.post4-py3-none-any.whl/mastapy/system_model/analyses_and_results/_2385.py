"""_2385.py

ModalAnalysisAtASpeed
"""


from mastapy.system_model.analyses_and_results import _2369
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisAtASpeed',)


class ModalAnalysisAtASpeed(_2369.SingleAnalysis):
    """ModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'ModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
