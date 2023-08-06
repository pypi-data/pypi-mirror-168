"""_946.py

KlingelnbergConicalGearSetDesign
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.conical import _1122, _1110
from mastapy.gears.gear_designs.klingelnberg_conical import _945
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CONICAL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergConical', 'KlingelnbergConicalGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalGearSetDesign',)


class KlingelnbergConicalGearSetDesign(_1110.ConicalGearSetDesign):
    """KlingelnbergConicalGearSetDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CONICAL_GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum_modification_factor(self) -> 'float':
        """float: 'AddendumModificationFactor' is the original name of this property."""

        temp = self.wrapped.AddendumModificationFactor

        if temp is None:
            return None

        return temp

    @addendum_modification_factor.setter
    def addendum_modification_factor(self, value: 'float'):
        self.wrapped.AddendumModificationFactor = float(value) if value else 0.0

    @property
    def addendum_of_tool(self) -> 'float':
        """float: 'AddendumOfTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AddendumOfTool

        if temp is None:
            return None

        return temp

    @property
    def angle_modification(self) -> 'float':
        """float: 'AngleModification' is the original name of this property."""

        temp = self.wrapped.AngleModification

        if temp is None:
            return None

        return temp

    @angle_modification.setter
    def angle_modification(self, value: 'float'):
        self.wrapped.AngleModification = float(value) if value else 0.0

    @property
    def auxiliary_value_for_angle_modification(self) -> 'float':
        """float: 'AuxiliaryValueForAngleModification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryValueForAngleModification

        if temp is None:
            return None

        return temp

    @property
    def auxiliary_angle_at_re(self) -> 'float':
        """float: 'AuxiliaryAngleAtRe' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryAngleAtRe

        if temp is None:
            return None

        return temp

    @property
    def auxiliary_angle_at_ri(self) -> 'float':
        """float: 'AuxiliaryAngleAtRi' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryAngleAtRi

        if temp is None:
            return None

        return temp

    @property
    def auxilliary_angle_at_re_2(self) -> 'float':
        """float: 'AuxilliaryAngleAtRe2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxilliaryAngleAtRe2

        if temp is None:
            return None

        return temp

    @property
    def auxilliary_angle_at_ri_2(self) -> 'float':
        """float: 'AuxilliaryAngleAtRi2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxilliaryAngleAtRi2

        if temp is None:
            return None

        return temp

    @property
    def base_circle_radius(self) -> 'float':
        """float: 'BaseCircleRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseCircleRadius

        if temp is None:
            return None

        return temp

    @property
    def cone_distance_maximum_tooth_gap(self) -> 'float':
        """float: 'ConeDistanceMaximumToothGap' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConeDistanceMaximumToothGap

        if temp is None:
            return None

        return temp

    @property
    def cutter_blade_tip_width_causes_cut_off(self) -> 'bool':
        """bool: 'CutterBladeTipWidthCausesCutOff' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterBladeTipWidthCausesCutOff

        if temp is None:
            return None

        return temp

    @property
    def cutter_blade_tip_width_causes_ridge(self) -> 'bool':
        """bool: 'CutterBladeTipWidthCausesRidge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterBladeTipWidthCausesRidge

        if temp is None:
            return None

        return temp

    @property
    def cutter_module(self) -> 'float':
        """float: 'CutterModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterModule

        if temp is None:
            return None

        return temp

    @property
    def cutter_radius(self) -> 'float':
        """float: 'CutterRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterRadius

        if temp is None:
            return None

        return temp

    @property
    def effective_face_width(self) -> 'float':
        """float: 'EffectiveFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def face_contact_ratio(self) -> 'float':
        """float: 'FaceContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceContactRatio

        if temp is None:
            return None

        return temp

    @property
    def gear_cutting_machine_options(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'GearCuttingMachineOptions' is the original name of this property."""

        temp = self.wrapped.GearCuttingMachineOptions

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @gear_cutting_machine_options.setter
    def gear_cutting_machine_options(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.GearCuttingMachineOptions = value

    @property
    def gear_finish(self) -> '_1122.KlingelnbergFinishingMethods':
        """KlingelnbergFinishingMethods: 'GearFinish' is the original name of this property."""

        temp = self.wrapped.GearFinish

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1122.KlingelnbergFinishingMethods)(value) if value is not None else None

    @gear_finish.setter
    def gear_finish(self, value: '_1122.KlingelnbergFinishingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearFinish = value

    @property
    def lead_angle_on_cutter_head(self) -> 'float':
        """float: 'LeadAngleOnCutterHead' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadAngleOnCutterHead

        if temp is None:
            return None

        return temp

    @property
    def machine_distance(self) -> 'float':
        """float: 'MachineDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MachineDistance

        if temp is None:
            return None

        return temp

    @property
    def module(self) -> 'float':
        """float: 'Module' is the original name of this property."""

        temp = self.wrapped.Module

        if temp is None:
            return None

        return temp

    @module.setter
    def module(self, value: 'float'):
        self.wrapped.Module = float(value) if value else 0.0

    @property
    def normal_module_at_inner_diameter(self) -> 'float':
        """float: 'NormalModuleAtInnerDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalModuleAtInnerDiameter

        if temp is None:
            return None

        return temp

    @property
    def normal_module_at_outer_diameter(self) -> 'float':
        """float: 'NormalModuleAtOuterDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalModuleAtOuterDiameter

        if temp is None:
            return None

        return temp

    @property
    def normal_pressure_angle_at_tooth_tip(self) -> 'float':
        """float: 'NormalPressureAngleAtToothTip' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalPressureAngleAtToothTip

        if temp is None:
            return None

        return temp

    @property
    def number_of_starts(self) -> 'float':
        """float: 'NumberOfStarts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfStarts

        if temp is None:
            return None

        return temp

    @property
    def pinion_generating_cone_angle(self) -> 'float':
        """float: 'PinionGeneratingConeAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionGeneratingConeAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_number_of_teeth(self) -> 'int':
        """int: 'PinionNumberOfTeeth' is the original name of this property."""

        temp = self.wrapped.PinionNumberOfTeeth

        if temp is None:
            return None

        return temp

    @pinion_number_of_teeth.setter
    def pinion_number_of_teeth(self, value: 'int'):
        self.wrapped.PinionNumberOfTeeth = int(value) if value else 0

    @property
    def shaft_angle(self) -> 'float':
        """float: 'ShaftAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftAngle

        if temp is None:
            return None

        return temp

    @property
    def spiral_angle_at_wheel_inner_diameter(self) -> 'float':
        """float: 'SpiralAngleAtWheelInnerDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralAngleAtWheelInnerDiameter

        if temp is None:
            return None

        return temp

    @property
    def spiral_angle_at_wheel_outer_diameter(self) -> 'float':
        """float: 'SpiralAngleAtWheelOuterDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralAngleAtWheelOuterDiameter

        if temp is None:
            return None

        return temp

    @property
    def stub_factor(self) -> 'float':
        """float: 'StubFactor' is the original name of this property."""

        temp = self.wrapped.StubFactor

        if temp is None:
            return None

        return temp

    @stub_factor.setter
    def stub_factor(self, value: 'float'):
        self.wrapped.StubFactor = float(value) if value else 0.0

    @property
    def tip_circle_diameter_of_virtual_gear(self) -> 'float':
        """float: 'TipCircleDiameterOfVirtualGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipCircleDiameterOfVirtualGear

        if temp is None:
            return None

        return temp

    @property
    def tip_cone_angle_from_tooth_tip_chamfering_reduction(self) -> 'float':
        """float: 'TipConeAngleFromToothTipChamferingReduction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipConeAngleFromToothTipChamferingReduction

        if temp is None:
            return None

        return temp

    @property
    def tooth_thickness_half_angle_on_pitch_cone(self) -> 'float':
        """float: 'ToothThicknessHalfAngleOnPitchCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessHalfAngleOnPitchCone

        if temp is None:
            return None

        return temp

    @property
    def tooth_thickness_half_angle_on_tooth_tip(self) -> 'float':
        """float: 'ToothThicknessHalfAngleOnToothTip' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessHalfAngleOnToothTip

        if temp is None:
            return None

        return temp

    @property
    def tooth_thickness_modification_factor(self) -> 'float':
        """float: 'ToothThicknessModificationFactor' is the original name of this property."""

        temp = self.wrapped.ToothThicknessModificationFactor

        if temp is None:
            return None

        return temp

    @tooth_thickness_modification_factor.setter
    def tooth_thickness_modification_factor(self, value: 'float'):
        self.wrapped.ToothThicknessModificationFactor = float(value) if value else 0.0

    @property
    def tooth_tip_chamfering_factor(self) -> 'float':
        """float: 'ToothTipChamferingFactor' is the original name of this property."""

        temp = self.wrapped.ToothTipChamferingFactor

        if temp is None:
            return None

        return temp

    @tooth_tip_chamfering_factor.setter
    def tooth_tip_chamfering_factor(self, value: 'float'):
        self.wrapped.ToothTipChamferingFactor = float(value) if value else 0.0

    @property
    def tooth_tip_thickness_at_inner(self) -> 'float':
        """float: 'ToothTipThicknessAtInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothTipThicknessAtInner

        if temp is None:
            return None

        return temp

    @property
    def tooth_tip_thickness_at_mean_cone_distance(self) -> 'float':
        """float: 'ToothTipThicknessAtMeanConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothTipThicknessAtMeanConeDistance

        if temp is None:
            return None

        return temp

    @property
    def use_minimum_addendum_modification_factor(self) -> 'bool':
        """bool: 'UseMinimumAddendumModificationFactor' is the original name of this property."""

        temp = self.wrapped.UseMinimumAddendumModificationFactor

        if temp is None:
            return None

        return temp

    @use_minimum_addendum_modification_factor.setter
    def use_minimum_addendum_modification_factor(self, value: 'bool'):
        self.wrapped.UseMinimumAddendumModificationFactor = bool(value) if value else False

    @property
    def use_required_tooth_tip_chamfering_factor(self) -> 'bool':
        """bool: 'UseRequiredToothTipChamferingFactor' is the original name of this property."""

        temp = self.wrapped.UseRequiredToothTipChamferingFactor

        if temp is None:
            return None

        return temp

    @use_required_tooth_tip_chamfering_factor.setter
    def use_required_tooth_tip_chamfering_factor(self, value: 'bool'):
        self.wrapped.UseRequiredToothTipChamferingFactor = bool(value) if value else False

    @property
    def wheel_face_width(self) -> 'float':
        """float: 'WheelFaceWidth' is the original name of this property."""

        temp = self.wrapped.WheelFaceWidth

        if temp is None:
            return None

        return temp

    @wheel_face_width.setter
    def wheel_face_width(self, value: 'float'):
        self.wrapped.WheelFaceWidth = float(value) if value else 0.0

    @property
    def wheel_generating_cone_angle(self) -> 'float':
        """float: 'WheelGeneratingConeAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelGeneratingConeAngle

        if temp is None:
            return None

        return temp

    @property
    def wheel_mean_spiral_angle(self) -> 'float':
        """float: 'WheelMeanSpiralAngle' is the original name of this property."""

        temp = self.wrapped.WheelMeanSpiralAngle

        if temp is None:
            return None

        return temp

    @wheel_mean_spiral_angle.setter
    def wheel_mean_spiral_angle(self, value: 'float'):
        self.wrapped.WheelMeanSpiralAngle = float(value) if value else 0.0

    @property
    def wheel_number_of_teeth(self) -> 'int':
        """int: 'WheelNumberOfTeeth' is the original name of this property."""

        temp = self.wrapped.WheelNumberOfTeeth

        if temp is None:
            return None

        return temp

    @wheel_number_of_teeth.setter
    def wheel_number_of_teeth(self, value: 'int'):
        self.wrapped.WheelNumberOfTeeth = int(value) if value else 0

    @property
    def wheel_pitch_diameter(self) -> 'float':
        """float: 'WheelPitchDiameter' is the original name of this property."""

        temp = self.wrapped.WheelPitchDiameter

        if temp is None:
            return None

        return temp

    @wheel_pitch_diameter.setter
    def wheel_pitch_diameter(self, value: 'float'):
        self.wrapped.WheelPitchDiameter = float(value) if value else 0.0

    @property
    def whole_depth(self) -> 'float':
        """float: 'WholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WholeDepth

        if temp is None:
            return None

        return temp

    @property
    def conical_meshes(self) -> 'List[_945.KlingelnbergConicalGearMeshDesign]':
        """List[KlingelnbergConicalGearMeshDesign]: 'ConicalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConicalMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_conical_meshes(self) -> 'List[_945.KlingelnbergConicalGearMeshDesign]':
        """List[KlingelnbergConicalGearMeshDesign]: 'KlingelnbergConicalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergConicalMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
