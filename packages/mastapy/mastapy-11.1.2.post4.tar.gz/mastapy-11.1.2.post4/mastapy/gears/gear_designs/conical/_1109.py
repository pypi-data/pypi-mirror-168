"""_1109.py

ConicalGearMeshDesign
"""


from mastapy.gears.gear_designs.bevel import _1141, _1138, _1142
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs import _912
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshDesign',)


class ConicalGearMeshDesign(_912.GearMeshDesign):
    """ConicalGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'ConicalGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def driven_machine_characteristic(self) -> '_1141.MachineCharacteristicAGMAKlingelnberg':
        """MachineCharacteristicAGMAKlingelnberg: 'DrivenMachineCharacteristic' is the original name of this property."""

        temp = self.wrapped.DrivenMachineCharacteristic

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1141.MachineCharacteristicAGMAKlingelnberg)(value) if value is not None else None

    @driven_machine_characteristic.setter
    def driven_machine_characteristic(self, value: '_1141.MachineCharacteristicAGMAKlingelnberg'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DrivenMachineCharacteristic = value

    @property
    def driven_machine_characteristic_gleason(self) -> '_1138.DrivenMachineCharacteristicGleason':
        """DrivenMachineCharacteristicGleason: 'DrivenMachineCharacteristicGleason' is the original name of this property."""

        temp = self.wrapped.DrivenMachineCharacteristicGleason

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1138.DrivenMachineCharacteristicGleason)(value) if value is not None else None

    @driven_machine_characteristic_gleason.setter
    def driven_machine_characteristic_gleason(self, value: '_1138.DrivenMachineCharacteristicGleason'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DrivenMachineCharacteristicGleason = value

    @property
    def maximum_normal_backlash(self) -> 'float':
        """float: 'MaximumNormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalBacklash

        if temp is None:
            return None

        return temp

    @property
    def minimum_normal_backlash(self) -> 'float':
        """float: 'MinimumNormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumNormalBacklash

        if temp is None:
            return None

        return temp

    @property
    def overload_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OverloadFactor' is the original name of this property."""

        temp = self.wrapped.OverloadFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @overload_factor.setter
    def overload_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OverloadFactor = value

    @property
    def pinion_full_circle_edge_radius(self) -> 'float':
        """float: 'PinionFullCircleEdgeRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionFullCircleEdgeRadius

        if temp is None:
            return None

        return temp

    @property
    def prime_mover_characteristic(self) -> '_1141.MachineCharacteristicAGMAKlingelnberg':
        """MachineCharacteristicAGMAKlingelnberg: 'PrimeMoverCharacteristic' is the original name of this property."""

        temp = self.wrapped.PrimeMoverCharacteristic

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1141.MachineCharacteristicAGMAKlingelnberg)(value) if value is not None else None

    @prime_mover_characteristic.setter
    def prime_mover_characteristic(self, value: '_1141.MachineCharacteristicAGMAKlingelnberg'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PrimeMoverCharacteristic = value

    @property
    def prime_mover_characteristic_gleason(self) -> '_1142.PrimeMoverCharacteristicGleason':
        """PrimeMoverCharacteristicGleason: 'PrimeMoverCharacteristicGleason' is the original name of this property."""

        temp = self.wrapped.PrimeMoverCharacteristicGleason

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1142.PrimeMoverCharacteristicGleason)(value) if value is not None else None

    @prime_mover_characteristic_gleason.setter
    def prime_mover_characteristic_gleason(self, value: '_1142.PrimeMoverCharacteristicGleason'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PrimeMoverCharacteristicGleason = value

    @property
    def shaft_angle(self) -> 'float':
        """float: 'ShaftAngle' is the original name of this property."""

        temp = self.wrapped.ShaftAngle

        if temp is None:
            return None

        return temp

    @shaft_angle.setter
    def shaft_angle(self, value: 'float'):
        self.wrapped.ShaftAngle = float(value) if value else 0.0

    @property
    def specified_backlash_range_max(self) -> 'float':
        """float: 'SpecifiedBacklashRangeMax' is the original name of this property."""

        temp = self.wrapped.SpecifiedBacklashRangeMax

        if temp is None:
            return None

        return temp

    @specified_backlash_range_max.setter
    def specified_backlash_range_max(self, value: 'float'):
        self.wrapped.SpecifiedBacklashRangeMax = float(value) if value else 0.0

    @property
    def specified_backlash_range_min(self) -> 'float':
        """float: 'SpecifiedBacklashRangeMin' is the original name of this property."""

        temp = self.wrapped.SpecifiedBacklashRangeMin

        if temp is None:
            return None

        return temp

    @specified_backlash_range_min.setter
    def specified_backlash_range_min(self, value: 'float'):
        self.wrapped.SpecifiedBacklashRangeMin = float(value) if value else 0.0

    @property
    def specify_backlash(self) -> 'bool':
        """bool: 'SpecifyBacklash' is the original name of this property."""

        temp = self.wrapped.SpecifyBacklash

        if temp is None:
            return None

        return temp

    @specify_backlash.setter
    def specify_backlash(self, value: 'bool'):
        self.wrapped.SpecifyBacklash = bool(value) if value else False
