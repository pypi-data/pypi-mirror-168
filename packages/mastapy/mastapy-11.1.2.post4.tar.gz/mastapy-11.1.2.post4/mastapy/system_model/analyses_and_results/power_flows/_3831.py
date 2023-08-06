"""_3831.py

FEPartPowerFlow
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2203
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.power_flows import _3775
from mastapy._internal.python_net import python_net_import

_FE_PART_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FEPartPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartPowerFlow',)


class FEPartPowerFlow(_3775.AbstractShaftOrHousingPowerFlow):
    """FEPartPowerFlow

    This is a mastapy class.
    """

    TYPE = _FE_PART_POWER_FLOW

    def __init__(self, instance_to_wrap: 'FEPartPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_parts_are_not_used_in_power_flow(self) -> 'str':
        """str: 'FEPartsAreNotUsedInPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEPartsAreNotUsedInPowerFlow

        if temp is None:
            return None

        return temp

    @property
    def fe_parts_are_not_used_in_power_flow_select_component_replaced_by_this_fe(self) -> 'str':
        """str: 'FEPartsAreNotUsedInPowerFlowSelectComponentReplacedByThisFE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEPartsAreNotUsedInPowerFlowSelectComponentReplacedByThisFE

        if temp is None:
            return None

        return temp

    @property
    def speed(self) -> 'float':
        """float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Speed

        if temp is None:
            return None

        return temp

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6611.FEPartLoadCase':
        """FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
