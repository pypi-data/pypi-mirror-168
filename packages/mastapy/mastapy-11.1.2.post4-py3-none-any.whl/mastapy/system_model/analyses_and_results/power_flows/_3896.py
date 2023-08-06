"""_3896.py

TorqueConverterPowerFlow
"""


from mastapy.system_model.part_model.couplings import _2356
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6701
from mastapy.system_model.analyses_and_results.power_flows import _3813
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'TorqueConverterPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPowerFlow',)


class TorqueConverterPowerFlow(_3813.CouplingPowerFlow):
    """TorqueConverterPowerFlow

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_POWER_FLOW

    def __init__(self, instance_to_wrap: 'TorqueConverterPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2356.TorqueConverter':
        """TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6701.TorqueConverterLoadCase':
        """TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
