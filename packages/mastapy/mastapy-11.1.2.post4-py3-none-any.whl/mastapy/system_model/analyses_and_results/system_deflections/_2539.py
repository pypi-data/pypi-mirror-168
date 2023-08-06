"""_2539.py

RingPinsToDiscConnectionSystemDeflection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.cycloidal import _2092
from mastapy.system_model.analyses_and_results.static_loads import _6671
from mastapy.system_model.analyses_and_results.power_flows import _3867
from mastapy.system_model.analyses_and_results.system_deflections import _2540, _2511
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RingPinsToDiscConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionSystemDeflection',)


class RingPinsToDiscConnectionSystemDeflection(_2511.InterMountableComponentConnectionSystemDeflection):
    """RingPinsToDiscConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_contact_stress_across_all_pins(self) -> 'float':
        """float: 'MaximumContactStressAcrossAllPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumContactStressAcrossAllPins

        if temp is None:
            return None

        return temp

    @property
    def normal_deflections(self) -> 'List[float]':
        """List[float]: 'NormalDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def number_of_pins_in_contact(self) -> 'int':
        """int: 'NumberOfPinsInContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfPinsInContact

        if temp is None:
            return None

        return temp

    @property
    def pin_with_maximum_contact_stress(self) -> 'int':
        """int: 'PinWithMaximumContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinWithMaximumContactStress

        if temp is None:
            return None

        return temp

    @property
    def strain_energy(self) -> 'float':
        """float: 'StrainEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrainEnergy

        if temp is None:
            return None

        return temp

    @property
    def connection_design(self) -> '_2092.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6671.RingPinsToDiscConnectionLoadCase':
        """RingPinsToDiscConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_3867.RingPinsToDiscConnectionPowerFlow':
        """RingPinsToDiscConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ring_pin_to_disc_contacts(self) -> 'List[_2540.RingPinToDiscContactReporting]':
        """List[RingPinToDiscContactReporting]: 'RingPinToDiscContacts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPinToDiscContacts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
