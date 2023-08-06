"""_638.py

HobbingProcessSimulationInput
"""


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _624, _642, _643, _651
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_SIMULATION_INPUT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessSimulationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessSimulationInput',)


class HobbingProcessSimulationInput(_651.ProcessSimulationInput):
    """HobbingProcessSimulationInput

    This is a mastapy class.
    """

    TYPE = _HOBBING_PROCESS_SIMULATION_INPUT

    def __init__(self, instance_to_wrap: 'HobbingProcessSimulationInput.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def process_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod':
        """enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod: 'ProcessMethod' is the original name of this property."""

        temp = self.wrapped.ProcessMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @process_method.setter
    def process_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ProcessMethod = value

    @property
    def hob_manufacture_error(self) -> '_642.HobManufactureError':
        """HobManufactureError: 'HobManufactureError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HobManufactureError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hob_resharpening_error(self) -> '_643.HobResharpeningError':
        """HobResharpeningError: 'HobResharpeningError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HobResharpeningError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
