"""_1149.py

AGMAGleasonConicalGearSetDesign
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.gears.gear_designs.bevel import _1133
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gleason_smt_link import _279
from mastapy.gears import _317, _320
from mastapy.gears.gear_designs.conical import _1119, _1110
from mastapy.gears.gear_designs.agma_gleason_conical import _1148
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetDesign',)


class AGMAGleasonConicalGearSetDesign(_1110.ConicalGearSetDesign):
    """AGMAGleasonConicalGearSetDesign

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def crown_gear_to_cutter_centre_distance(self) -> 'float':
        """float: 'CrownGearToCutterCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CrownGearToCutterCentreDistance

        if temp is None:
            return None

        return temp

    @property
    def design_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods':
        """enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods: 'DesignMethod' is the original name of this property."""

        temp = self.wrapped.DesignMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @design_method.setter
    def design_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DesignMethod = value

    @property
    def epicycloid_base_circle_radius(self) -> 'float':
        """float: 'EpicycloidBaseCircleRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EpicycloidBaseCircleRadius

        if temp is None:
            return None

        return temp

    @property
    def gleason_minimum_factor_of_safety_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'GleasonMinimumFactorOfSafetyBending' is the original name of this property."""

        temp = self.wrapped.GleasonMinimumFactorOfSafetyBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @gleason_minimum_factor_of_safety_bending.setter
    def gleason_minimum_factor_of_safety_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.GleasonMinimumFactorOfSafetyBending = value

    @property
    def gleason_minimum_factor_of_safety_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'GleasonMinimumFactorOfSafetyContact' is the original name of this property."""

        temp = self.wrapped.GleasonMinimumFactorOfSafetyContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @gleason_minimum_factor_of_safety_contact.setter
    def gleason_minimum_factor_of_safety_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.GleasonMinimumFactorOfSafetyContact = value

    @property
    def input_module(self) -> 'bool':
        """bool: 'InputModule' is the original name of this property."""

        temp = self.wrapped.InputModule

        if temp is None:
            return None

        return temp

    @input_module.setter
    def input_module(self, value: 'bool'):
        self.wrapped.InputModule = bool(value) if value else False

    @property
    def manufacturing_method(self) -> '_279.CutterMethod':
        """CutterMethod: 'ManufacturingMethod' is the original name of this property."""

        temp = self.wrapped.ManufacturingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_279.CutterMethod)(value) if value is not None else None

    @manufacturing_method.setter
    def manufacturing_method(self, value: '_279.CutterMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ManufacturingMethod = value

    @property
    def mean_normal_module(self) -> 'float':
        """float: 'MeanNormalModule' is the original name of this property."""

        temp = self.wrapped.MeanNormalModule

        if temp is None:
            return None

        return temp

    @mean_normal_module.setter
    def mean_normal_module(self, value: 'float'):
        self.wrapped.MeanNormalModule = float(value) if value else 0.0

    @property
    def number_of_blade_groups(self) -> 'float':
        """float: 'NumberOfBladeGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfBladeGroups

        if temp is None:
            return None

        return temp

    @property
    def number_of_crown_gear_teeth(self) -> 'float':
        """float: 'NumberOfCrownGearTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfCrownGearTeeth

        if temp is None:
            return None

        return temp

    @property
    def pinion_offset_angle_in_root_plane(self) -> 'float':
        """float: 'PinionOffsetAngleInRootPlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionOffsetAngleInRootPlane

        if temp is None:
            return None

        return temp

    @property
    def pitch_limit_pressure_angle(self) -> 'float':
        """float: 'PitchLimitPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchLimitPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def reliability_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ReliabilityFactorBending' is the original name of this property."""

        temp = self.wrapped.ReliabilityFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @reliability_factor_bending.setter
    def reliability_factor_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ReliabilityFactorBending = value

    @property
    def reliability_factor_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ReliabilityFactorContact' is the original name of this property."""

        temp = self.wrapped.ReliabilityFactorContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @reliability_factor_contact.setter
    def reliability_factor_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ReliabilityFactorContact = value

    @property
    def reliability_requirement_agma(self) -> '_317.SafetyRequirementsAGMA':
        """SafetyRequirementsAGMA: 'ReliabilityRequirementAGMA' is the original name of this property."""

        temp = self.wrapped.ReliabilityRequirementAGMA

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_317.SafetyRequirementsAGMA)(value) if value is not None else None

    @reliability_requirement_agma.setter
    def reliability_requirement_agma(self, value: '_317.SafetyRequirementsAGMA'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ReliabilityRequirementAGMA = value

    @property
    def reliability_requirement_gleason(self) -> '_1119.GleasonSafetyRequirements':
        """GleasonSafetyRequirements: 'ReliabilityRequirementGleason' is the original name of this property."""

        temp = self.wrapped.ReliabilityRequirementGleason

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1119.GleasonSafetyRequirements)(value) if value is not None else None

    @reliability_requirement_gleason.setter
    def reliability_requirement_gleason(self, value: '_1119.GleasonSafetyRequirements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ReliabilityRequirementGleason = value

    @property
    def required_minimum_topland_to_module_factor(self) -> 'float':
        """float: 'RequiredMinimumToplandToModuleFactor' is the original name of this property."""

        temp = self.wrapped.RequiredMinimumToplandToModuleFactor

        if temp is None:
            return None

        return temp

    @required_minimum_topland_to_module_factor.setter
    def required_minimum_topland_to_module_factor(self, value: 'float'):
        self.wrapped.RequiredMinimumToplandToModuleFactor = float(value) if value else 0.0

    @property
    def tooth_taper(self) -> '_320.SpiralBevelToothTaper':
        """SpiralBevelToothTaper: 'ToothTaper' is the original name of this property."""

        temp = self.wrapped.ToothTaper

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_320.SpiralBevelToothTaper)(value) if value is not None else None

    @tooth_taper.setter
    def tooth_taper(self, value: '_320.SpiralBevelToothTaper'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothTaper = value

    @property
    def wheel_involute_cone_distance(self) -> 'float':
        """float: 'WheelInvoluteConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInvoluteConeDistance

        if temp is None:
            return None

        return temp

    @property
    def wheel_involute_to_mean_cone_distance_ratio(self) -> 'float':
        """float: 'WheelInvoluteToMeanConeDistanceRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInvoluteToMeanConeDistanceRatio

        if temp is None:
            return None

        return temp

    @property
    def wheel_involute_to_outer_cone_distance_ratio(self) -> 'float':
        """float: 'WheelInvoluteToOuterConeDistanceRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInvoluteToOuterConeDistanceRatio

        if temp is None:
            return None

        return temp

    @property
    def conical_meshes(self) -> 'List[_1148.AGMAGleasonConicalGearMeshDesign]':
        """List[AGMAGleasonConicalGearMeshDesign]: 'ConicalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConicalMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshes(self) -> 'List[_1148.AGMAGleasonConicalGearMeshDesign]':
        """List[AGMAGleasonConicalGearMeshDesign]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Meshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def export_ki_mo_skip_file(self):
        """ 'ExportKIMoSKIPFile' is the original name of this method."""

        self.wrapped.ExportKIMoSKIPFile()

    def gleason_gemsxml_data(self):
        """ 'GleasonGEMSXMLData' is the original name of this method."""

        self.wrapped.GleasonGEMSXMLData()

    def ki_mo_sxml_data(self):
        """ 'KIMoSXMLData' is the original name of this method."""

        self.wrapped.KIMoSXMLData()

    def store_ki_mo_skip_file(self):
        """ 'StoreKIMoSKIPFile' is the original name of this method."""

        self.wrapped.StoreKIMoSKIPFile()
