"""_1047.py

ToothThicknessSpecificationBase
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _996
from mastapy.utility.units_and_measurements.measurements import _1460, _1476
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TOOTH_THICKNESS_SPECIFICATION_BASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ToothThicknessSpecificationBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothThicknessSpecificationBase',)


class ToothThicknessSpecificationBase(_0.APIBase):
    """ToothThicknessSpecificationBase

    This is a mastapy class.
    """

    TYPE = _TOOTH_THICKNESS_SPECIFICATION_BASE

    def __init__(self, instance_to_wrap: 'ToothThicknessSpecificationBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ball_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BallDiameter' is the original name of this property."""

        temp = self.wrapped.BallDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @ball_diameter.setter
    def ball_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BallDiameter = value

    @property
    def ball_diameter_at_form_diameter(self) -> 'float':
        """float: 'BallDiameterAtFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BallDiameterAtFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def ball_diameter_at_tip_form_diameter(self) -> 'float':
        """float: 'BallDiameterAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BallDiameterAtTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def diameter_at_thickness_measurement(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DiameterAtThicknessMeasurement' is the original name of this property."""

        temp = self.wrapped.DiameterAtThicknessMeasurement

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @diameter_at_thickness_measurement.setter
    def diameter_at_thickness_measurement(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DiameterAtThicknessMeasurement = value

    @property
    def maximum_number_of_teeth_for_chordal_span_test(self) -> 'int':
        """int: 'MaximumNumberOfTeethForChordalSpanTest' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNumberOfTeethForChordalSpanTest

        if temp is None:
            return None

        return temp

    @property
    def minimum_number_of_teeth_for_chordal_span_test(self) -> 'int':
        """int: 'MinimumNumberOfTeethForChordalSpanTest' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumNumberOfTeethForChordalSpanTest

        if temp is None:
            return None

        return temp

    @property
    def number_of_teeth_for_chordal_span_test(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfTeethForChordalSpanTest' is the original name of this property."""

        temp = self.wrapped.NumberOfTeethForChordalSpanTest

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_teeth_for_chordal_span_test.setter
    def number_of_teeth_for_chordal_span_test(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfTeethForChordalSpanTest = value

    @property
    def chordal_span(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'ChordalSpan' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChordalSpan

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def normal_thickness(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'NormalThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThickness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def normal_thickness_at_specified_diameter(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'NormalThicknessAtSpecifiedDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtSpecifiedDiameter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def over_balls(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'OverBalls' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverBalls

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def profile_shift(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'ProfileShift' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileShift

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def profile_shift_coefficient(self) -> '_996.CylindricalGearToothThicknessSpecification[_1476.Number]':
        """CylindricalGearToothThicknessSpecification[Number]: 'ProfileShiftCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileShiftCoefficient

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1476.Number](temp) if temp is not None else None

    @property
    def transverse_thickness(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'TransverseThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseThickness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def transverse_thickness_at_specified_diameter(self) -> '_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]':
        """CylindricalGearToothThicknessSpecification[LengthShort]: 'TransverseThicknessAtSpecifiedDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseThicknessAtSpecifiedDiameter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1460.LengthShort](temp) if temp is not None else None

    @property
    def tooth_thickness(self) -> 'List[_996.CylindricalGearToothThicknessSpecification[_1460.LengthShort]]':
        """List[CylindricalGearToothThicknessSpecification[LengthShort]]: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThickness

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
