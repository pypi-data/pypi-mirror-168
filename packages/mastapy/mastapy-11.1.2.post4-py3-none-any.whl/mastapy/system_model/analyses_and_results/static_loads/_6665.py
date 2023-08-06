"""_6665.py

PointLoadLoadCase
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.varying_input_components import _91, _92
from mastapy.system_model.part_model import _2221
from mastapy.system_model.analyses_and_results.static_loads import _6664, _6709
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PointLoadLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadLoadCase',)


class PointLoadLoadCase(_6709.VirtualComponentLoadCase):
    """PointLoadLoadCase

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_LOAD_CASE

    def __init__(self, instance_to_wrap: 'PointLoadLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_of_radial_force(self) -> 'float':
        """float: 'AngleOfRadialForce' is the original name of this property."""

        temp = self.wrapped.AngleOfRadialForce

        if temp is None:
            return None

        return temp

    @angle_of_radial_force.setter
    def angle_of_radial_force(self, value: 'float'):
        self.wrapped.AngleOfRadialForce = float(value) if value else 0.0

    @property
    def displacement_x(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DisplacementX' is the original name of this property."""

        temp = self.wrapped.DisplacementX

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @displacement_x.setter
    def displacement_x(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DisplacementX = value

    @property
    def displacement_y(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DisplacementY' is the original name of this property."""

        temp = self.wrapped.DisplacementY

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @displacement_y.setter
    def displacement_y(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DisplacementY = value

    @property
    def displacement_z(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DisplacementZ' is the original name of this property."""

        temp = self.wrapped.DisplacementZ

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @displacement_z.setter
    def displacement_z(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DisplacementZ = value

    @property
    def force_specification_options(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification':
        """enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification: 'ForceSpecificationOptions' is the original name of this property."""

        temp = self.wrapped.ForceSpecificationOptions

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @force_specification_options.setter
    def force_specification_options(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ForceSpecificationOptions = value

    @property
    def magnitude_radial_force(self) -> 'float':
        """float: 'MagnitudeRadialForce' is the original name of this property."""

        temp = self.wrapped.MagnitudeRadialForce

        if temp is None:
            return None

        return temp

    @magnitude_radial_force.setter
    def magnitude_radial_force(self, value: 'float'):
        self.wrapped.MagnitudeRadialForce = float(value) if value else 0.0

    @property
    def radial_load(self) -> 'float':
        """float: 'RadialLoad' is the original name of this property."""

        temp = self.wrapped.RadialLoad

        if temp is None:
            return None

        return temp

    @radial_load.setter
    def radial_load(self, value: 'float'):
        self.wrapped.RadialLoad = float(value) if value else 0.0

    @property
    def tangential_load(self) -> 'float':
        """float: 'TangentialLoad' is the original name of this property."""

        temp = self.wrapped.TangentialLoad

        if temp is None:
            return None

        return temp

    @tangential_load.setter
    def tangential_load(self, value: 'float'):
        self.wrapped.TangentialLoad = float(value) if value else 0.0

    @property
    def twist_theta_x(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TwistThetaX' is the original name of this property."""

        temp = self.wrapped.TwistThetaX

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @twist_theta_x.setter
    def twist_theta_x(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TwistThetaX = value

    @property
    def twist_theta_y(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TwistThetaY' is the original name of this property."""

        temp = self.wrapped.TwistThetaY

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @twist_theta_y.setter
    def twist_theta_y(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TwistThetaY = value

    @property
    def twist_theta_z(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TwistThetaZ' is the original name of this property."""

        temp = self.wrapped.TwistThetaZ

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @twist_theta_z.setter
    def twist_theta_z(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TwistThetaZ = value

    @property
    def axial_load(self) -> '_91.ForceInputComponent':
        """ForceInputComponent: 'AxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design(self) -> '_2221.PointLoad':
        """PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force_x(self) -> '_91.ForceInputComponent':
        """ForceInputComponent: 'ForceX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceX

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force_y(self) -> '_91.ForceInputComponent':
        """ForceInputComponent: 'ForceY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceY

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def moment_x(self) -> '_92.MomentInputComponent':
        """MomentInputComponent: 'MomentX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MomentX

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def moment_y(self) -> '_92.MomentInputComponent':
        """MomentInputComponent: 'MomentY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MomentY

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def moment_z(self) -> '_92.MomentInputComponent':
        """MomentInputComponent: 'MomentZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MomentZ

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def get_harmonic_load_data_for_import(self) -> '_6664.PointLoadHarmonicLoadData':
        """ 'GetHarmonicLoadDataForImport' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadHarmonicLoadData
        """

        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
