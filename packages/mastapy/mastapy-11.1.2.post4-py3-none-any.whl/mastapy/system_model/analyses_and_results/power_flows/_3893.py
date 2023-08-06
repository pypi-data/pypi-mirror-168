"""_3893.py

SynchroniserSleevePowerFlow
"""


from mastapy.system_model.part_model.couplings import _2355
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6698
from mastapy.system_model.analyses_and_results.power_flows import _3891
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SynchroniserSleevePowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleevePowerFlow',)


class SynchroniserSleevePowerFlow(_3891.SynchroniserPartPowerFlow):
    """SynchroniserSleevePowerFlow

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_SLEEVE_POWER_FLOW

    def __init__(self, instance_to_wrap: 'SynchroniserSleevePowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6698.SynchroniserSleeveLoadCase':
        """SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
