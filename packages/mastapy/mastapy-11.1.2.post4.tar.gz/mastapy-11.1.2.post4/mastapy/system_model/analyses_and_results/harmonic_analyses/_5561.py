"""_5561.py

UnbalancedMassExcitationDetail
"""


from mastapy.system_model.analyses_and_results.harmonic_analyses import _5536
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'UnbalancedMassExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassExcitationDetail',)


class UnbalancedMassExcitationDetail(_5536.SingleNodePeriodicExcitationWithReferenceShaft):
    """UnbalancedMassExcitationDetail

    This is a mastapy class.
    """

    TYPE = _UNBALANCED_MASS_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'UnbalancedMassExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
