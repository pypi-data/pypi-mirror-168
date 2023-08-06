"""_2101.py

SpringDamperConnection
"""


from mastapy.system_model import _1958
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.nodal_analysis import _69
from mastapy.system_model.connections_and_sockets.couplings import _2097
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnection',)


class SpringDamperConnection(_2097.CouplingConnection):
    """SpringDamperConnection

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_CONNECTION

    def __init__(self, instance_to_wrap: 'SpringDamperConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def damping_option(self) -> '_1958.ComponentDampingOption':
        """ComponentDampingOption: 'DampingOption' is the original name of this property."""

        temp = self.wrapped.DampingOption

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1958.ComponentDampingOption)(value) if value is not None else None

    @damping_option.setter
    def damping_option(self, value: '_1958.ComponentDampingOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DampingOption = value

    @property
    def damping(self) -> '_69.LinearDampingConnectionProperties':
        """LinearDampingConnectionProperties: 'Damping' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Damping

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
