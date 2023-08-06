"""_7095.py

RollingRingConnectionAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.connections_and_sockets import _2043
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6673
from mastapy.system_model.analyses_and_results.system_deflections import _2542
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7066
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'RollingRingConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionAdvancedSystemDeflection',)


class RollingRingConnectionAdvancedSystemDeflection(_7066.InterMountableComponentConnectionAdvancedSystemDeflection):
    """RollingRingConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'RollingRingConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2043.RollingRingConnection':
        """RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6673.RollingRingConnectionLoadCase':
        """RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2542.RollingRingConnectionSystemDeflection]':
        """List[RollingRingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionAdvancedSystemDeflection]':
        """List[RollingRingConnectionAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
