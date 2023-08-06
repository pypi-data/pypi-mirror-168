"""_4456.py

DesignEntityModalAnalysisGroupResults
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DESIGN_ENTITY_MODAL_ANALYSIS_GROUP_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'DesignEntityModalAnalysisGroupResults')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignEntityModalAnalysisGroupResults',)


class DesignEntityModalAnalysisGroupResults(_0.APIBase):
    """DesignEntityModalAnalysisGroupResults

    This is a mastapy class.
    """

    TYPE = _DESIGN_ENTITY_MODAL_ANALYSIS_GROUP_RESULTS

    def __init__(self, instance_to_wrap: 'DesignEntityModalAnalysisGroupResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp
