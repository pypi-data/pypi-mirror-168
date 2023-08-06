"""_3881.py

SpringDamperPowerFlow
"""


from mastapy.system_model.part_model.couplings import _2349
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6686
from mastapy.system_model.analyses_and_results.power_flows import _3813
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SpringDamperPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperPowerFlow',)


class SpringDamperPowerFlow(_3813.CouplingPowerFlow):
    """SpringDamperPowerFlow

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_POWER_FLOW

    def __init__(self, instance_to_wrap: 'SpringDamperPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2349.SpringDamper':
        """SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6686.SpringDamperLoadCase':
        """SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
