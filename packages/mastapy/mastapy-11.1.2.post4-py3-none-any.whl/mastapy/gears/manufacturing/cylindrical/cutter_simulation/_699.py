"""_699.py

CylindricalGearSpecification
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import (
    _1047, _1007, _1027, _1046
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CylindricalGearSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSpecification',)


class CylindricalGearSpecification(_0.APIBase):
    """CylindricalGearSpecification

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SPECIFICATION

    def __init__(self, instance_to_wrap: 'CylindricalGearSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def helix_angle(self) -> 'float':
        """float: 'HelixAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngle

        if temp is None:
            return None

        return temp

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
    def normal_module(self) -> 'float':
        """float: 'NormalModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalModule

        if temp is None:
            return None

        return temp

    @property
    def normal_pressure_angle(self) -> 'float':
        """float: 'NormalPressureAngle' is the original name of this property."""

        temp = self.wrapped.NormalPressureAngle

        if temp is None:
            return None

        return temp

    @normal_pressure_angle.setter
    def normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalPressureAngle = float(value) if value else 0.0

    @property
    def number_of_teeth_unsigned(self) -> 'float':
        """float: 'NumberOfTeethUnsigned' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfTeethUnsigned

        if temp is None:
            return None

        return temp

    @property
    def tooth_thickness_specification(self) -> '_1047.ToothThicknessSpecificationBase':
        """ToothThicknessSpecificationBase: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessSpecification

        if temp is None:
            return None

        if _1047.ToothThicknessSpecificationBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to ToothThicknessSpecificationBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness_specification_of_type_finish_tooth_thickness_design_specification(self) -> '_1007.FinishToothThicknessDesignSpecification':
        """FinishToothThicknessDesignSpecification: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessSpecification

        if temp is None:
            return None

        if _1007.FinishToothThicknessDesignSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to FinishToothThicknessDesignSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness_specification_of_type_readonly_tooth_thickness_specification(self) -> '_1027.ReadonlyToothThicknessSpecification':
        """ReadonlyToothThicknessSpecification: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessSpecification

        if temp is None:
            return None

        if _1027.ReadonlyToothThicknessSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to ReadonlyToothThicknessSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_thickness_specification_of_type_tooth_thickness_specification(self) -> '_1046.ToothThicknessSpecification':
        """ToothThicknessSpecification: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessSpecification

        if temp is None:
            return None

        if _1046.ToothThicknessSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to ToothThicknessSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
