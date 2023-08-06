"""_6669.py

RingPinManufacturingError
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.tolerances import _1682
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RING_PIN_MANUFACTURING_ERROR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RingPinManufacturingError')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinManufacturingError',)


class RingPinManufacturingError(_0.APIBase):
    """RingPinManufacturingError

    This is a mastapy class.
    """

    TYPE = _RING_PIN_MANUFACTURING_ERROR

    def __init__(self, instance_to_wrap: 'RingPinManufacturingError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def override_all_pins_roundness_specification(self) -> 'bool':
        """bool: 'OverrideAllPinsRoundnessSpecification' is the original name of this property."""

        temp = self.wrapped.OverrideAllPinsRoundnessSpecification

        if temp is None:
            return None

        return temp

    @override_all_pins_roundness_specification.setter
    def override_all_pins_roundness_specification(self, value: 'bool'):
        self.wrapped.OverrideAllPinsRoundnessSpecification = bool(value) if value else False

    @property
    def pin_angular_position_error(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PinAngularPositionError' is the original name of this property."""

        temp = self.wrapped.PinAngularPositionError

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pin_angular_position_error.setter
    def pin_angular_position_error(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PinAngularPositionError = value

    @property
    def pin_diameter_error(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PinDiameterError' is the original name of this property."""

        temp = self.wrapped.PinDiameterError

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pin_diameter_error.setter
    def pin_diameter_error(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PinDiameterError = value

    @property
    def pin_radial_position_error(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PinRadialPositionError' is the original name of this property."""

        temp = self.wrapped.PinRadialPositionError

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @pin_radial_position_error.setter
    def pin_radial_position_error(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PinRadialPositionError = value

    @property
    def pin_roundness_chart(self) -> 'Image':
        """Image: 'PinRoundnessChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinRoundnessChart

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def show_pin_roundness_chart(self) -> 'bool':
        """bool: 'ShowPinRoundnessChart' is the original name of this property."""

        temp = self.wrapped.ShowPinRoundnessChart

        if temp is None:
            return None

        return temp

    @show_pin_roundness_chart.setter
    def show_pin_roundness_chart(self, value: 'bool'):
        self.wrapped.ShowPinRoundnessChart = bool(value) if value else False

    @property
    def roundness_specification(self) -> '_1682.RoundnessSpecification':
        """RoundnessSpecification: 'RoundnessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoundnessSpecification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
