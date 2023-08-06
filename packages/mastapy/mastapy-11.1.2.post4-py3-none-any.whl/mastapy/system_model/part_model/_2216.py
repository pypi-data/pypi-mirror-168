"""_2216.py

OilSeal
"""


from mastapy.math_utility import _1341
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.materials.efficiency import _274, _275
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_results import _1723
from mastapy.system_model.part_model import _2198
from mastapy._internal.python_net import python_net_import

_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSeal',)


class OilSeal(_2198.Connector):
    """OilSeal

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL

    def __init__(self, instance_to_wrap: 'OilSeal.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def drag_torque_vs_rotational_speed(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'DragTorqueVsRotationalSpeed' is the original name of this property."""

        temp = self.wrapped.DragTorqueVsRotationalSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @drag_torque_vs_rotational_speed.setter
    def drag_torque_vs_rotational_speed(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.DragTorqueVsRotationalSpeed = value

    @property
    def intercept_of_linear_equation_defining_the_effect_of_temperature(self) -> 'float':
        """float: 'InterceptOfLinearEquationDefiningTheEffectOfTemperature' is the original name of this property."""

        temp = self.wrapped.InterceptOfLinearEquationDefiningTheEffectOfTemperature

        if temp is None:
            return None

        return temp

    @intercept_of_linear_equation_defining_the_effect_of_temperature.setter
    def intercept_of_linear_equation_defining_the_effect_of_temperature(self, value: 'float'):
        self.wrapped.InterceptOfLinearEquationDefiningTheEffectOfTemperature = float(value) if value else 0.0

    @property
    def oil_seal_characteristic_life(self) -> 'float':
        """float: 'OilSealCharacteristicLife' is the original name of this property."""

        temp = self.wrapped.OilSealCharacteristicLife

        if temp is None:
            return None

        return temp

    @oil_seal_characteristic_life.setter
    def oil_seal_characteristic_life(self, value: 'float'):
        self.wrapped.OilSealCharacteristicLife = float(value) if value else 0.0

    @property
    def oil_seal_frictional_torque(self) -> 'float':
        """float: 'OilSealFrictionalTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilSealFrictionalTorque

        if temp is None:
            return None

        return temp

    @property
    def oil_seal_loss_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod: 'OilSealLossCalculationMethod' is the original name of this property."""

        temp = self.wrapped.OilSealLossCalculationMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @oil_seal_loss_calculation_method.setter
    def oil_seal_loss_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_OilSealLossCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.OilSealLossCalculationMethod = value

    @property
    def oil_seal_material(self) -> '_275.OilSealMaterialType':
        """OilSealMaterialType: 'OilSealMaterial' is the original name of this property."""

        temp = self.wrapped.OilSealMaterial

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_275.OilSealMaterialType)(value) if value is not None else None

    @oil_seal_material.setter
    def oil_seal_material(self, value: '_275.OilSealMaterialType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilSealMaterial = value

    @property
    def oil_seal_mean_time_before_failure(self) -> 'float':
        """float: 'OilSealMeanTimeBeforeFailure' is the original name of this property."""

        temp = self.wrapped.OilSealMeanTimeBeforeFailure

        if temp is None:
            return None

        return temp

    @oil_seal_mean_time_before_failure.setter
    def oil_seal_mean_time_before_failure(self, value: 'float'):
        self.wrapped.OilSealMeanTimeBeforeFailure = float(value) if value else 0.0

    @property
    def oil_seal_orientation(self) -> '_1723.Orientations':
        """Orientations: 'OilSealOrientation' is the original name of this property."""

        temp = self.wrapped.OilSealOrientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1723.Orientations)(value) if value is not None else None

    @oil_seal_orientation.setter
    def oil_seal_orientation(self, value: '_1723.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilSealOrientation = value

    @property
    def slope_of_linear_equation_defining_the_effect_of_temperature(self) -> 'float':
        """float: 'SlopeOfLinearEquationDefiningTheEffectOfTemperature' is the original name of this property."""

        temp = self.wrapped.SlopeOfLinearEquationDefiningTheEffectOfTemperature

        if temp is None:
            return None

        return temp

    @slope_of_linear_equation_defining_the_effect_of_temperature.setter
    def slope_of_linear_equation_defining_the_effect_of_temperature(self, value: 'float'):
        self.wrapped.SlopeOfLinearEquationDefiningTheEffectOfTemperature = float(value) if value else 0.0

    @property
    def width(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @width.setter
    def width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Width = value
