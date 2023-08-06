"""_5258.py

DynamicForceResultAtTime
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5257
from mastapy._internal.python_net import python_net_import

_DYNAMIC_FORCE_RESULT_AT_TIME = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Reporting', 'DynamicForceResultAtTime')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicForceResultAtTime',)


class DynamicForceResultAtTime(_5257.AbstractMeasuredDynamicResponseAtTime):
    """DynamicForceResultAtTime

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_FORCE_RESULT_AT_TIME

    def __init__(self, instance_to_wrap: 'DynamicForceResultAtTime.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_dynamic_force(self) -> 'float':
        """float: 'AbsoluteDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteDynamicForce

        if temp is None:
            return None

        return temp

    @property
    def dynamic_force(self) -> 'float':
        """float: 'DynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicForce

        if temp is None:
            return None

        return temp

    @property
    def force(self) -> 'float':
        """float: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Force

        if temp is None:
            return None

        return temp

    @property
    def mean_force(self) -> 'float':
        """float: 'MeanForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanForce

        if temp is None:
            return None

        return temp
