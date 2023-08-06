"""_4459.py

RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4460
from mastapy._internal.python_net import python_net_import

_RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_FOR_SINGLE_EXCITATION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis',)


class RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis(_4460.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis):
    """RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis

    This is a mastapy class.
    """

    TYPE = _RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_FOR_SINGLE_EXCITATION_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def reference_speed_of_crossing(self) -> 'float':
        """float: 'ReferenceSpeedOfCrossing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceSpeedOfCrossing

        if temp is None:
            return None

        return temp
