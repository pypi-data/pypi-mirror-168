"""_557.py

CylindricalGearMaterial
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.materials import _568, _560
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'CylindricalGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMaterial',)


class CylindricalGearMaterial(_560.GearMaterial):
    """CylindricalGearMaterial

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MATERIAL

    def __init__(self, instance_to_wrap: 'CylindricalGearMaterial.TYPE'):
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
    def allowable_stress_number_contact(self) -> 'float':
        """float: 'AllowableStressNumberContact' is the original name of this property."""

        temp = self.wrapped.AllowableStressNumberContact

        if temp is None:
            return None

        return temp

    @allowable_stress_number_contact.setter
    def allowable_stress_number_contact(self, value: 'float'):
        self.wrapped.AllowableStressNumberContact = float(value) if value else 0.0

    @property
    def heat_conductivity(self) -> 'float':
        """float: 'HeatConductivity' is the original name of this property."""

        temp = self.wrapped.HeatConductivity

        if temp is None:
            return None

        return temp

    @heat_conductivity.setter
    def heat_conductivity(self, value: 'float'):
        self.wrapped.HeatConductivity = float(value) if value else 0.0

    @property
    def heat_treatment_distortion_control(self) -> '_568.ManufactureRating':
        """ManufactureRating: 'HeatTreatmentDistortionControl' is the original name of this property."""

        temp = self.wrapped.HeatTreatmentDistortionControl

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_568.ManufactureRating)(value) if value is not None else None

    @heat_treatment_distortion_control.setter
    def heat_treatment_distortion_control(self, value: '_568.ManufactureRating'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HeatTreatmentDistortionControl = value

    @property
    def heat_treatment_process_development(self) -> '_568.ManufactureRating':
        """ManufactureRating: 'HeatTreatmentProcessDevelopment' is the original name of this property."""

        temp = self.wrapped.HeatTreatmentProcessDevelopment

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_568.ManufactureRating)(value) if value is not None else None

    @heat_treatment_process_development.setter
    def heat_treatment_process_development(self, value: '_568.ManufactureRating'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HeatTreatmentProcessDevelopment = value

    @property
    def machine_process_development(self) -> '_568.ManufactureRating':
        """ManufactureRating: 'MachineProcessDevelopment' is the original name of this property."""

        temp = self.wrapped.MachineProcessDevelopment

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_568.ManufactureRating)(value) if value is not None else None

    @machine_process_development.setter
    def machine_process_development(self, value: '_568.ManufactureRating'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MachineProcessDevelopment = value

    @property
    def manufacturability(self) -> '_568.ManufactureRating':
        """ManufactureRating: 'Manufacturability' is the original name of this property."""

        temp = self.wrapped.Manufacturability

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_568.ManufactureRating)(value) if value is not None else None

    @manufacturability.setter
    def manufacturability(self, value: '_568.ManufactureRating'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Manufacturability = value

    @property
    def material_type(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'MaterialType' is the original name of this property."""

        temp = self.wrapped.MaterialType

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @material_type.setter
    def material_type(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.MaterialType = value

    @property
    def nominal_stress_number_bending(self) -> 'float':
        """float: 'NominalStressNumberBending' is the original name of this property."""

        temp = self.wrapped.NominalStressNumberBending

        if temp is None:
            return None

        return temp

    @nominal_stress_number_bending.setter
    def nominal_stress_number_bending(self, value: 'float'):
        self.wrapped.NominalStressNumberBending = float(value) if value else 0.0

    @property
    def retained_austenite(self) -> 'float':
        """float: 'RetainedAustenite' is the original name of this property."""

        temp = self.wrapped.RetainedAustenite

        if temp is None:
            return None

        return temp

    @retained_austenite.setter
    def retained_austenite(self, value: 'float'):
        self.wrapped.RetainedAustenite = float(value) if value else 0.0

    @property
    def sn_curve_bending_allowable_stress_point_selector(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'SNCurveBendingAllowableStressPointSelector' is the original name of this property."""

        temp = self.wrapped.SNCurveBendingAllowableStressPointSelector

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @sn_curve_bending_allowable_stress_point_selector.setter
    def sn_curve_bending_allowable_stress_point_selector(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.SNCurveBendingAllowableStressPointSelector = value

    @property
    def sn_curve_contact_allowable_stress_point_selector(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'SNCurveContactAllowableStressPointSelector' is the original name of this property."""

        temp = self.wrapped.SNCurveContactAllowableStressPointSelector

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @sn_curve_contact_allowable_stress_point_selector.setter
    def sn_curve_contact_allowable_stress_point_selector(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.SNCurveContactAllowableStressPointSelector = value

    @property
    def shot_peened(self) -> 'bool':
        """bool: 'ShotPeened' is the original name of this property."""

        temp = self.wrapped.ShotPeened

        if temp is None:
            return None

        return temp

    @shot_peened.setter
    def shot_peened(self, value: 'bool'):
        self.wrapped.ShotPeened = bool(value) if value else False

    @property
    def specific_heat(self) -> 'float':
        """float: 'SpecificHeat' is the original name of this property."""

        temp = self.wrapped.SpecificHeat

        if temp is None:
            return None

        return temp

    @specific_heat.setter
    def specific_heat(self, value: 'float'):
        self.wrapped.SpecificHeat = float(value) if value else 0.0

    @property
    def specify_allowable_stress_number_bending(self) -> 'bool':
        """bool: 'SpecifyAllowableStressNumberBending' is the original name of this property."""

        temp = self.wrapped.SpecifyAllowableStressNumberBending

        if temp is None:
            return None

        return temp

    @specify_allowable_stress_number_bending.setter
    def specify_allowable_stress_number_bending(self, value: 'bool'):
        self.wrapped.SpecifyAllowableStressNumberBending = bool(value) if value else False

    @property
    def specify_allowable_stress_number_contact(self) -> 'bool':
        """bool: 'SpecifyAllowableStressNumberContact' is the original name of this property."""

        temp = self.wrapped.SpecifyAllowableStressNumberContact

        if temp is None:
            return None

        return temp

    @specify_allowable_stress_number_contact.setter
    def specify_allowable_stress_number_contact(self, value: 'bool'):
        self.wrapped.SpecifyAllowableStressNumberContact = bool(value) if value else False

    @property
    def welding_structural_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'WeldingStructuralFactor' is the original name of this property."""

        temp = self.wrapped.WeldingStructuralFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @welding_structural_factor.setter
    def welding_structural_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WeldingStructuralFactor = value
