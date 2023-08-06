"""_2543.py

RollingRingSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2345
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6674
from mastapy.system_model.analyses_and_results.power_flows import _3870
from mastapy.system_model.analyses_and_results.system_deflections import _2474
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RollingRingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingSystemDeflection',)


class RollingRingSystemDeflection(_2474.CouplingHalfSystemDeflection):
    """RollingRingSystemDeflection

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'RollingRingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2345.RollingRing':
        """RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6674.RollingRingLoadCase':
        """RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_3870.RollingRingPowerFlow':
        """RollingRingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingSystemDeflection]':
        """List[RollingRingSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
