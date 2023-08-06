"""_1061.py

CylindricalGearMicroGeometryMap
"""


from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1074
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_MAP = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMicroGeometryMap')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroGeometryMap',)


class CylindricalGearMicroGeometryMap(_0.APIBase):
    """CylindricalGearMicroGeometryMap

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_MAP

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroGeometryMap.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def measured_map_data_type(self) -> '_1074.MeasuredMapDataTypes':
        """MeasuredMapDataTypes: 'MeasuredMapDataType' is the original name of this property."""

        temp = self.wrapped.MeasuredMapDataType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1074.MeasuredMapDataTypes)(value) if value is not None else None

    @measured_map_data_type.setter
    def measured_map_data_type(self, value: '_1074.MeasuredMapDataTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MeasuredMapDataType = value

    @property
    def profile_factor_for_0_bias_relief(self) -> 'float':
        """float: 'ProfileFactorFor0BiasRelief' is the original name of this property."""

        temp = self.wrapped.ProfileFactorFor0BiasRelief

        if temp is None:
            return None

        return temp

    @profile_factor_for_0_bias_relief.setter
    def profile_factor_for_0_bias_relief(self, value: 'float'):
        self.wrapped.ProfileFactorFor0BiasRelief = float(value) if value else 0.0

    @property
    def zero_bias_relief(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ZeroBiasRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZeroBiasRelief

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def switch_measured_data_direction_with_respect_to_face_width(self):
        """ 'SwitchMeasuredDataDirectionWithRespectToFaceWidth' is the original name of this method."""

        self.wrapped.SwitchMeasuredDataDirectionWithRespectToFaceWidth()
