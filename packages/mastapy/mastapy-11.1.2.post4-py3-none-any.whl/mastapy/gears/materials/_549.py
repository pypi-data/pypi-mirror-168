"""_549.py

AGMACylindricalGearMaterial
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.materials import _220, _218, _219
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.materials import _557
from mastapy._internal.python_net import python_net_import

_AGMA_CYLINDRICAL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'AGMACylindricalGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMACylindricalGearMaterial',)


class AGMACylindricalGearMaterial(_557.CylindricalGearMaterial):
    """AGMACylindricalGearMaterial

    This is a mastapy class.
    """

    TYPE = _AGMA_CYLINDRICAL_GEAR_MATERIAL

    def __init__(self, instance_to_wrap: 'AGMACylindricalGearMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_stress_number_bending(self) -> 'float':
        """float: 'AllowableStressNumberBending' is the original name of this property."""

        temp = self.wrapped.AllowableStressNumberBending

        if temp is None:
            return None

        return temp

    @allowable_stress_number_bending.setter
    def allowable_stress_number_bending(self, value: 'float'):
        self.wrapped.AllowableStressNumberBending = float(value) if value else 0.0

    @property
    def grade(self) -> '_220.AGMAMaterialGrade':
        """AGMAMaterialGrade: 'Grade' is the original name of this property."""

        temp = self.wrapped.Grade

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_220.AGMAMaterialGrade)(value) if value is not None else None

    @grade.setter
    def grade(self, value: '_220.AGMAMaterialGrade'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Grade = value

    @property
    def material_application(self) -> '_218.AGMAMaterialApplications':
        """AGMAMaterialApplications: 'MaterialApplication' is the original name of this property."""

        temp = self.wrapped.MaterialApplication

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_218.AGMAMaterialApplications)(value) if value is not None else None

    @material_application.setter
    def material_application(self, value: '_218.AGMAMaterialApplications'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialApplication = value

    @property
    def material_class(self) -> '_219.AGMAMaterialClasses':
        """AGMAMaterialClasses: 'MaterialClass' is the original name of this property."""

        temp = self.wrapped.MaterialClass

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_219.AGMAMaterialClasses)(value) if value is not None else None

    @material_class.setter
    def material_class(self, value: '_219.AGMAMaterialClasses'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialClass = value

    @property
    def stress_cycle_factor_at_1e10_cycles_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'StressCycleFactorAt1E10CyclesBending' is the original name of this property."""

        temp = self.wrapped.StressCycleFactorAt1E10CyclesBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @stress_cycle_factor_at_1e10_cycles_bending.setter
    def stress_cycle_factor_at_1e10_cycles_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.StressCycleFactorAt1E10CyclesBending = value

    @property
    def stress_cycle_factor_at_1e10_cycles_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'StressCycleFactorAt1E10CyclesContact' is the original name of this property."""

        temp = self.wrapped.StressCycleFactorAt1E10CyclesContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @stress_cycle_factor_at_1e10_cycles_contact.setter
    def stress_cycle_factor_at_1e10_cycles_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.StressCycleFactorAt1E10CyclesContact = value
