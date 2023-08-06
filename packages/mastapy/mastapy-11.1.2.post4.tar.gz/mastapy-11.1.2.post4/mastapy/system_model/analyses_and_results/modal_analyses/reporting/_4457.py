"""_4457.py

ModalCMSResultsForModeAndFE
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.component_mode_synthesis import _210
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MODAL_CMS_RESULTS_FOR_MODE_AND_FE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'ModalCMSResultsForModeAndFE')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalCMSResultsForModeAndFE',)


class ModalCMSResultsForModeAndFE(_0.APIBase):
    """ModalCMSResultsForModeAndFE

    This is a mastapy class.
    """

    TYPE = _MODAL_CMS_RESULTS_FOR_MODE_AND_FE

    def __init__(self, instance_to_wrap: 'ModalCMSResultsForModeAndFE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_name(self) -> 'str':
        """str: 'FEName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEName

        if temp is None:
            return None

        return temp

    @property
    def modal_full_fe_results(self) -> '_210.ModalCMSResults':
        """ModalCMSResults: 'ModalFullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModalFullFEResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
