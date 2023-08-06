"""_6671.py

RingPinsToDiscConnectionLoadCase
"""


from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.math_utility.hertzian_contact import _1378
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.system_model.connections_and_sockets.cycloidal import _2092
from mastapy.system_model.analyses_and_results.static_loads import _6637
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RingPinsToDiscConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionLoadCase',)


class RingPinsToDiscConnectionLoadCase(_6637.InterMountableComponentConnectionLoadCase):
    """RingPinsToDiscConnectionLoadCase

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION_LOAD_CASE

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hertzian_contact_deflection_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod: 'HertzianContactDeflectionCalculationMethod' is the original name of this property."""

        temp = self.wrapped.HertzianContactDeflectionCalculationMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @hertzian_contact_deflection_calculation_method.setter
    def hertzian_contact_deflection_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.HertzianContactDeflectionCalculationMethod = value

    @property
    def number_of_lobes_passed(self) -> 'float':
        """float: 'NumberOfLobesPassed' is the original name of this property."""

        temp = self.wrapped.NumberOfLobesPassed

        if temp is None:
            return None

        return temp

    @number_of_lobes_passed.setter
    def number_of_lobes_passed(self, value: 'float'):
        self.wrapped.NumberOfLobesPassed = float(value) if value else 0.0

    @property
    def number_of_steps_for_one_lobe_pass(self) -> 'int':
        """int: 'NumberOfStepsForOneLobePass' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfStepsForOneLobePass

        if temp is None:
            return None

        return temp

    @property
    def specified_contact_stiffness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SpecifiedContactStiffness' is the original name of this property."""

        temp = self.wrapped.SpecifiedContactStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @specified_contact_stiffness.setter
    def specified_contact_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpecifiedContactStiffness = value

    @property
    def use_constant_mesh_stiffness(self) -> 'bool':
        """bool: 'UseConstantMeshStiffness' is the original name of this property."""

        temp = self.wrapped.UseConstantMeshStiffness

        if temp is None:
            return None

        return temp

    @use_constant_mesh_stiffness.setter
    def use_constant_mesh_stiffness(self, value: 'bool'):
        self.wrapped.UseConstantMeshStiffness = bool(value) if value else False

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
