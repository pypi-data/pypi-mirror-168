"""_5395.py

ClutchEngagementStatus
"""


from mastapy.system_model.analyses_and_results.load_case_groups import _5399
from mastapy.system_model.connections_and_sockets.couplings import _2093
from mastapy._internal.python_net import python_net_import

_CLUTCH_ENGAGEMENT_STATUS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'ClutchEngagementStatus')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchEngagementStatus',)


class ClutchEngagementStatus(_5399.GenericClutchEngagementStatus['_2093.ClutchConnection']):
    """ClutchEngagementStatus

    This is a mastapy class.
    """

    TYPE = _CLUTCH_ENGAGEMENT_STATUS

    def __init__(self, instance_to_wrap: 'ClutchEngagementStatus.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
