"""_5260.py

DynamicTorqueResultAtTime
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5257
from mastapy._internal.python_net import python_net_import

_DYNAMIC_TORQUE_RESULT_AT_TIME = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Reporting', 'DynamicTorqueResultAtTime')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicTorqueResultAtTime',)


class DynamicTorqueResultAtTime(_5257.AbstractMeasuredDynamicResponseAtTime):
    """DynamicTorqueResultAtTime

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_TORQUE_RESULT_AT_TIME

    def __init__(self, instance_to_wrap: 'DynamicTorqueResultAtTime.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_dynamic_torque(self) -> 'float':
        """float: 'AbsoluteDynamicTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteDynamicTorque

        if temp is None:
            return None

        return temp

    @property
    def dynamic_torque(self) -> 'float':
        """float: 'DynamicTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicTorque

        if temp is None:
            return None

        return temp

    @property
    def mean_torque(self) -> 'float':
        """float: 'MeanTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTorque

        if temp is None:
            return None

        return temp

    @property
    def torque(self) -> 'float':
        """float: 'Torque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Torque

        if temp is None:
            return None

        return temp
