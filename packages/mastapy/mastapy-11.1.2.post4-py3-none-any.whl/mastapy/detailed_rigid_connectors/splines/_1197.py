"""_1197.py

CustomSplineHalfDesign
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.detailed_rigid_connectors.splines import _1222
from mastapy._internal.python_net import python_net_import

_CUSTOM_SPLINE_HALF_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'CustomSplineHalfDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomSplineHalfDesign',)


class CustomSplineHalfDesign(_1222.SplineHalfDesign):
    """CustomSplineHalfDesign

    This is a mastapy class.
    """

    TYPE = _CUSTOM_SPLINE_HALF_DESIGN

    def __init__(self, instance_to_wrap: 'CustomSplineHalfDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def actual_tooth_thickness_or_space_width_tolerance(self) -> 'float':
        """float: 'ActualToothThicknessOrSpaceWidthTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActualToothThicknessOrSpaceWidthTolerance

        if temp is None:
            return None

        return temp

    @property
    def addendum_factor(self) -> 'float':
        """float: 'AddendumFactor' is the original name of this property."""

        temp = self.wrapped.AddendumFactor

        if temp is None:
            return None

        return temp

    @addendum_factor.setter
    def addendum_factor(self, value: 'float'):
        self.wrapped.AddendumFactor = float(value) if value else 0.0

    @property
    def dedendum_factor(self) -> 'float':
        """float: 'DedendumFactor' is the original name of this property."""

        temp = self.wrapped.DedendumFactor

        if temp is None:
            return None

        return temp

    @dedendum_factor.setter
    def dedendum_factor(self, value: 'float'):
        self.wrapped.DedendumFactor = float(value) if value else 0.0

    @property
    def effective_tooth_thickness_or_space_width_tolerance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'EffectiveToothThicknessOrSpaceWidthTolerance' is the original name of this property."""

        temp = self.wrapped.EffectiveToothThicknessOrSpaceWidthTolerance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @effective_tooth_thickness_or_space_width_tolerance.setter
    def effective_tooth_thickness_or_space_width_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.EffectiveToothThicknessOrSpaceWidthTolerance = value

    @property
    def form_diameter(self) -> 'float':
        """float: 'FormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormDiameter

        if temp is None:
            return None

        return temp

    @property
    def major_diameter(self) -> 'float':
        """float: 'MajorDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MajorDiameter

        if temp is None:
            return None

        return temp

    @property
    def major_diameter_specified(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MajorDiameterSpecified' is the original name of this property."""

        temp = self.wrapped.MajorDiameterSpecified

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @major_diameter_specified.setter
    def major_diameter_specified(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MajorDiameterSpecified = value

    @property
    def maximum_actual_space_width(self) -> 'float':
        """float: 'MaximumActualSpaceWidth' is the original name of this property."""

        temp = self.wrapped.MaximumActualSpaceWidth

        if temp is None:
            return None

        return temp

    @maximum_actual_space_width.setter
    def maximum_actual_space_width(self, value: 'float'):
        self.wrapped.MaximumActualSpaceWidth = float(value) if value else 0.0

    @property
    def maximum_actual_tooth_thickness(self) -> 'float':
        """float: 'MaximumActualToothThickness' is the original name of this property."""

        temp = self.wrapped.MaximumActualToothThickness

        if temp is None:
            return None

        return temp

    @maximum_actual_tooth_thickness.setter
    def maximum_actual_tooth_thickness(self, value: 'float'):
        self.wrapped.MaximumActualToothThickness = float(value) if value else 0.0

    @property
    def maximum_chordal_span_over_teeth(self) -> 'float':
        """float: 'MaximumChordalSpanOverTeeth' is the original name of this property."""

        temp = self.wrapped.MaximumChordalSpanOverTeeth

        if temp is None:
            return None

        return temp

    @maximum_chordal_span_over_teeth.setter
    def maximum_chordal_span_over_teeth(self, value: 'float'):
        self.wrapped.MaximumChordalSpanOverTeeth = float(value) if value else 0.0

    @property
    def maximum_dimension_over_balls(self) -> 'float':
        """float: 'MaximumDimensionOverBalls' is the original name of this property."""

        temp = self.wrapped.MaximumDimensionOverBalls

        if temp is None:
            return None

        return temp

    @maximum_dimension_over_balls.setter
    def maximum_dimension_over_balls(self, value: 'float'):
        self.wrapped.MaximumDimensionOverBalls = float(value) if value else 0.0

    @property
    def maximum_effective_tooth_thickness(self) -> 'float':
        """float: 'MaximumEffectiveToothThickness' is the original name of this property."""

        temp = self.wrapped.MaximumEffectiveToothThickness

        if temp is None:
            return None

        return temp

    @maximum_effective_tooth_thickness.setter
    def maximum_effective_tooth_thickness(self, value: 'float'):
        self.wrapped.MaximumEffectiveToothThickness = float(value) if value else 0.0

    @property
    def maximum_space_width_deviation(self) -> 'float':
        """float: 'MaximumSpaceWidthDeviation' is the original name of this property."""

        temp = self.wrapped.MaximumSpaceWidthDeviation

        if temp is None:
            return None

        return temp

    @maximum_space_width_deviation.setter
    def maximum_space_width_deviation(self, value: 'float'):
        self.wrapped.MaximumSpaceWidthDeviation = float(value) if value else 0.0

    @property
    def maximum_tooth_thickness_deviation(self) -> 'float':
        """float: 'MaximumToothThicknessDeviation' is the original name of this property."""

        temp = self.wrapped.MaximumToothThicknessDeviation

        if temp is None:
            return None

        return temp

    @maximum_tooth_thickness_deviation.setter
    def maximum_tooth_thickness_deviation(self, value: 'float'):
        self.wrapped.MaximumToothThicknessDeviation = float(value) if value else 0.0

    @property
    def minimum_actual_space_width(self) -> 'float':
        """float: 'MinimumActualSpaceWidth' is the original name of this property."""

        temp = self.wrapped.MinimumActualSpaceWidth

        if temp is None:
            return None

        return temp

    @minimum_actual_space_width.setter
    def minimum_actual_space_width(self, value: 'float'):
        self.wrapped.MinimumActualSpaceWidth = float(value) if value else 0.0

    @property
    def minimum_actual_tooth_thickness(self) -> 'float':
        """float: 'MinimumActualToothThickness' is the original name of this property."""

        temp = self.wrapped.MinimumActualToothThickness

        if temp is None:
            return None

        return temp

    @minimum_actual_tooth_thickness.setter
    def minimum_actual_tooth_thickness(self, value: 'float'):
        self.wrapped.MinimumActualToothThickness = float(value) if value else 0.0

    @property
    def minimum_chordal_span_over_teeth(self) -> 'float':
        """float: 'MinimumChordalSpanOverTeeth' is the original name of this property."""

        temp = self.wrapped.MinimumChordalSpanOverTeeth

        if temp is None:
            return None

        return temp

    @minimum_chordal_span_over_teeth.setter
    def minimum_chordal_span_over_teeth(self, value: 'float'):
        self.wrapped.MinimumChordalSpanOverTeeth = float(value) if value else 0.0

    @property
    def minimum_dimension_over_balls(self) -> 'float':
        """float: 'MinimumDimensionOverBalls' is the original name of this property."""

        temp = self.wrapped.MinimumDimensionOverBalls

        if temp is None:
            return None

        return temp

    @minimum_dimension_over_balls.setter
    def minimum_dimension_over_balls(self, value: 'float'):
        self.wrapped.MinimumDimensionOverBalls = float(value) if value else 0.0

    @property
    def minimum_effective_space_width(self) -> 'float':
        """float: 'MinimumEffectiveSpaceWidth' is the original name of this property."""

        temp = self.wrapped.MinimumEffectiveSpaceWidth

        if temp is None:
            return None

        return temp

    @minimum_effective_space_width.setter
    def minimum_effective_space_width(self, value: 'float'):
        self.wrapped.MinimumEffectiveSpaceWidth = float(value) if value else 0.0

    @property
    def minimum_space_width_deviation(self) -> 'float':
        """float: 'MinimumSpaceWidthDeviation' is the original name of this property."""

        temp = self.wrapped.MinimumSpaceWidthDeviation

        if temp is None:
            return None

        return temp

    @minimum_space_width_deviation.setter
    def minimum_space_width_deviation(self, value: 'float'):
        self.wrapped.MinimumSpaceWidthDeviation = float(value) if value else 0.0

    @property
    def minimum_tooth_thickness_deviation(self) -> 'float':
        """float: 'MinimumToothThicknessDeviation' is the original name of this property."""

        temp = self.wrapped.MinimumToothThicknessDeviation

        if temp is None:
            return None

        return temp

    @minimum_tooth_thickness_deviation.setter
    def minimum_tooth_thickness_deviation(self, value: 'float'):
        self.wrapped.MinimumToothThicknessDeviation = float(value) if value else 0.0

    @property
    def minor_diameter(self) -> 'float':
        """float: 'MinorDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinorDiameter

        if temp is None:
            return None

        return temp

    @property
    def minor_diameter_specified(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinorDiameterSpecified' is the original name of this property."""

        temp = self.wrapped.MinorDiameterSpecified

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minor_diameter_specified.setter
    def minor_diameter_specified(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinorDiameterSpecified = value

    @property
    def root_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RootDiameter' is the original name of this property."""

        temp = self.wrapped.RootDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @root_diameter.setter
    def root_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RootDiameter = value

    @property
    def root_fillet_radius_factor(self) -> 'float':
        """float: 'RootFilletRadiusFactor' is the original name of this property."""

        temp = self.wrapped.RootFilletRadiusFactor

        if temp is None:
            return None

        return temp

    @root_fillet_radius_factor.setter
    def root_fillet_radius_factor(self, value: 'float'):
        self.wrapped.RootFilletRadiusFactor = float(value) if value else 0.0

    @property
    def tip_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TipDiameter' is the original name of this property."""

        temp = self.wrapped.TipDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tip_diameter.setter
    def tip_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TipDiameter = value

    @property
    def total_tooth_thickness_or_space_width_tolerance(self) -> 'float':
        """float: 'TotalToothThicknessOrSpaceWidthTolerance' is the original name of this property."""

        temp = self.wrapped.TotalToothThicknessOrSpaceWidthTolerance

        if temp is None:
            return None

        return temp

    @total_tooth_thickness_or_space_width_tolerance.setter
    def total_tooth_thickness_or_space_width_tolerance(self, value: 'float'):
        self.wrapped.TotalToothThicknessOrSpaceWidthTolerance = float(value) if value else 0.0
