"""_3868.py

RollingRingAssemblyPowerFlow
"""


from mastapy.system_model.part_model.couplings import _2346
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6672
from mastapy.system_model.analyses_and_results.power_flows import _3875
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RollingRingAssemblyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyPowerFlow',)


class RollingRingAssemblyPowerFlow(_3875.SpecialisedAssemblyPowerFlow):
    """RollingRingAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_ASSEMBLY_POWER_FLOW

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2346.RollingRingAssembly':
        """RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6672.RollingRingAssemblyLoadCase':
        """RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
