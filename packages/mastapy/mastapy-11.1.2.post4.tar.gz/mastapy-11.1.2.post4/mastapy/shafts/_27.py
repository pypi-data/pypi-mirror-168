"""_27.py

ShaftPointStressCycle
"""


from mastapy.shafts import _41, _26
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_POINT_STRESS_CYCLE = python_net_import('SMT.MastaAPI.Shafts', 'ShaftPointStressCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftPointStressCycle',)


class ShaftPointStressCycle(_0.APIBase):
    """ShaftPointStressCycle

    This is a mastapy class.
    """

    TYPE = _SHAFT_POINT_STRESS_CYCLE

    def __init__(self, instance_to_wrap: 'ShaftPointStressCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def din743201212_comparative_mean_stress(self) -> '_41.StressMeasurementShaftAxialBendingTorsionalComponentValues':
        """StressMeasurementShaftAxialBendingTorsionalComponentValues: 'DIN743201212ComparativeMeanStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DIN743201212ComparativeMeanStress

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stress_amplitude(self) -> '_26.ShaftPointStress':
        """ShaftPointStress: 'StressAmplitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAmplitude

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stress_mean(self) -> '_26.ShaftPointStress':
        """ShaftPointStress: 'StressMean' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressMean

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stress_total(self) -> '_26.ShaftPointStress':
        """ShaftPointStress: 'StressTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
