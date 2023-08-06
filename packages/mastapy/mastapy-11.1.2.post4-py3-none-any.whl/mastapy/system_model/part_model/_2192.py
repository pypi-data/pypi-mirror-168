"""_2192.py

BearingRaceMountingOptions
"""


from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings.bearing_results import _1726, _1727
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy._internal.python_net import python_net_import
from mastapy.materials import _223
from mastapy import _0

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_BEARING_RACE_MOUNTING_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BearingRaceMountingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRaceMountingOptions',)


class BearingRaceMountingOptions(_0.APIBase):
    """BearingRaceMountingOptions

    This is a mastapy class.
    """

    TYPE = _BEARING_RACE_MOUNTING_OPTIONS

    def __init__(self, instance_to_wrap: 'BearingRaceMountingOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_mounting(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType':
        """enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType: 'AxialMounting' is the original name of this property."""

        temp = self.wrapped.AxialMounting

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @axial_mounting.setter
    def axial_mounting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.AxialMounting = value

    @property
    def bore_mounting_sleeve(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BoreMountingSleeve' is the original name of this property."""

        temp = self.wrapped.BoreMountingSleeve

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @bore_mounting_sleeve.setter
    def bore_mounting_sleeve(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BoreMountingSleeve = value

    @property
    def has_mounting_sleeve(self) -> 'bool':
        """bool: 'HasMountingSleeve' is the original name of this property."""

        temp = self.wrapped.HasMountingSleeve

        if temp is None:
            return None

        return temp

    @has_mounting_sleeve.setter
    def has_mounting_sleeve(self, value: 'bool'):
        self.wrapped.HasMountingSleeve = bool(value) if value else False

    @property
    def left_axial_mounting_clearance(self) -> 'float':
        """float: 'LeftAxialMountingClearance' is the original name of this property."""

        temp = self.wrapped.LeftAxialMountingClearance

        if temp is None:
            return None

        return temp

    @left_axial_mounting_clearance.setter
    def left_axial_mounting_clearance(self, value: 'float'):
        self.wrapped.LeftAxialMountingClearance = float(value) if value else 0.0

    @property
    def mounting_sleeve_material_reportable(self) -> 'str':
        """str: 'MountingSleeveMaterialReportable' is the original name of this property."""

        temp = self.wrapped.MountingSleeveMaterialReportable.SelectedItemName

        if temp is None:
            return None

        return temp

    @mounting_sleeve_material_reportable.setter
    def mounting_sleeve_material_reportable(self, value: 'str'):
        self.wrapped.MountingSleeveMaterialReportable.SetSelectedItem(str(value) if value else '')

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
    def outer_diameter_mounting_sleeve(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OuterDiameterMountingSleeve' is the original name of this property."""

        temp = self.wrapped.OuterDiameterMountingSleeve

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @outer_diameter_mounting_sleeve.setter
    def outer_diameter_mounting_sleeve(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OuterDiameterMountingSleeve = value

    @property
    def radial_clearance_contact_stiffness(self) -> 'float':
        """float: 'RadialClearanceContactStiffness' is the original name of this property."""

        temp = self.wrapped.RadialClearanceContactStiffness

        if temp is None:
            return None

        return temp

    @radial_clearance_contact_stiffness.setter
    def radial_clearance_contact_stiffness(self, value: 'float'):
        self.wrapped.RadialClearanceContactStiffness = float(value) if value else 0.0

    @property
    def radial_mounting_clearance(self) -> 'float':
        """float: 'RadialMountingClearance' is the original name of this property."""

        temp = self.wrapped.RadialMountingClearance

        if temp is None:
            return None

        return temp

    @radial_mounting_clearance.setter
    def radial_mounting_clearance(self, value: 'float'):
        self.wrapped.RadialMountingClearance = float(value) if value else 0.0

    @property
    def right_axial_mounting_clearance(self) -> 'float':
        """float: 'RightAxialMountingClearance' is the original name of this property."""

        temp = self.wrapped.RightAxialMountingClearance

        if temp is None:
            return None

        return temp

    @right_axial_mounting_clearance.setter
    def right_axial_mounting_clearance(self, value: 'float'):
        self.wrapped.RightAxialMountingClearance = float(value) if value else 0.0

    @property
    def simple_radial_mounting(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType':
        """enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType: 'SimpleRadialMounting' is the original name of this property."""

        temp = self.wrapped.SimpleRadialMounting

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @simple_radial_mounting.setter
    def simple_radial_mounting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.SimpleRadialMounting = value

    @property
    def temperature_of_mounting_sleeve(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TemperatureOfMountingSleeve' is the original name of this property."""

        temp = self.wrapped.TemperatureOfMountingSleeve

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @temperature_of_mounting_sleeve.setter
    def temperature_of_mounting_sleeve(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TemperatureOfMountingSleeve = value

    @property
    def mounting_sleeve_material(self) -> '_223.BearingMaterial':
        """BearingMaterial: 'MountingSleeveMaterial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountingSleeveMaterial

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
