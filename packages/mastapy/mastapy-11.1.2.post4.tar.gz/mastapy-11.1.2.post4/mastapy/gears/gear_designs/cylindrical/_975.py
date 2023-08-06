"""_975.py

CylindricalGearDesign
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears import _305, _286
from mastapy.geometry.two_d import _284
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1090, _1092, _1088, _1089,
    _1091, _1093, _1096, _1097,
    _1098, _1094, _1099, _1095
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.agma_gleason_conical import _1146
from mastapy.gears.gear_designs.cylindrical import (
    _964, _973, _990, _1001,
    _1006, _1007, _1016, _1015,
    _1017, _1018, _981, _984,
    _1046, _1027, _1039, _1041,
    _982
)
from mastapy.gears.manufacturing.cylindrical import _578
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1059
from mastapy.gears.materials import (
    _560, _549, _551, _553,
    _557, _563, _567, _569
)
from mastapy.gears.gear_designs import _910

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesign',)


class CylindricalGearDesign(_910.GearDesign):
    """CylindricalGearDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_rim_diameter(self) -> 'float':
        """float: 'AbsoluteRimDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteRimDiameter

        if temp is None:
            return None

        return temp

    @property
    def addendum(self) -> 'float':
        """float: 'Addendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Addendum

        if temp is None:
            return None

        return temp

    @property
    def dedendum(self) -> 'float':
        """float: 'Dedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Dedendum

        if temp is None:
            return None

        return temp

    @property
    def effective_web_thickness(self) -> 'float':
        """float: 'EffectiveWebThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveWebThickness

        if temp is None:
            return None

        return temp

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property."""

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def factor_for_the_increase_of_the_yield_point_under_compression(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FactorForTheIncreaseOfTheYieldPointUnderCompression' is the original name of this property."""

        temp = self.wrapped.FactorForTheIncreaseOfTheYieldPointUnderCompression

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @factor_for_the_increase_of_the_yield_point_under_compression.setter
    def factor_for_the_increase_of_the_yield_point_under_compression(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FactorForTheIncreaseOfTheYieldPointUnderCompression = value

    @property
    def flank_heat_transfer_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FlankHeatTransferCoefficient' is the original name of this property."""

        temp = self.wrapped.FlankHeatTransferCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @flank_heat_transfer_coefficient.setter
    def flank_heat_transfer_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FlankHeatTransferCoefficient = value

    @property
    def gear_drawing(self) -> 'Image':
        """Image: 'GearDrawing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDrawing

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gear_hand(self) -> 'str':
        """str: 'GearHand' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearHand

        if temp is None:
            return None

        return temp

    @property
    def gear_tooth_drawing(self) -> 'Image':
        """Image: 'GearToothDrawing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearToothDrawing

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def hand(self) -> '_305.Hand':
        """Hand: 'Hand' is the original name of this property."""

        temp = self.wrapped.Hand

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_305.Hand)(value) if value is not None else None

    @hand.setter
    def hand(self, value: '_305.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Hand = value

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
    def helix_angle_at_tip_form_diameter(self) -> 'float':
        """float: 'HelixAngleAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleAtTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def initial_clocking_angle(self) -> 'float':
        """float: 'InitialClockingAngle' is the original name of this property."""

        temp = self.wrapped.InitialClockingAngle

        if temp is None:
            return None

        return temp

    @initial_clocking_angle.setter
    def initial_clocking_angle(self, value: 'float'):
        self.wrapped.InitialClockingAngle = float(value) if value else 0.0

    @property
    def internal_external(self) -> '_284.InternalExternalType':
        """InternalExternalType: 'InternalExternal' is the original name of this property."""

        temp = self.wrapped.InternalExternal

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_284.InternalExternalType)(value) if value is not None else None

    @internal_external.setter
    def internal_external(self, value: '_284.InternalExternalType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InternalExternal = value

    @property
    def is_asymmetric(self) -> 'bool':
        """bool: 'IsAsymmetric' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsAsymmetric

        if temp is None:
            return None

        return temp

    @property
    def lead(self) -> 'float':
        """float: 'Lead' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Lead

        if temp is None:
            return None

        return temp

    @property
    def mass(self) -> 'float':
        """float: 'Mass' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Mass

        if temp is None:
            return None

        return temp

    @property
    def material_agma(self) -> 'str':
        """str: 'MaterialAGMA' is the original name of this property."""

        temp = self.wrapped.MaterialAGMA.SelectedItemName

        if temp is None:
            return None

        return temp

    @material_agma.setter
    def material_agma(self, value: 'str'):
        self.wrapped.MaterialAGMA.SetSelectedItem(str(value) if value else '')

    @property
    def material_iso(self) -> 'str':
        """str: 'MaterialISO' is the original name of this property."""

        temp = self.wrapped.MaterialISO.SelectedItemName

        if temp is None:
            return None

        return temp

    @material_iso.setter
    def material_iso(self, value: 'str'):
        self.wrapped.MaterialISO.SetSelectedItem(str(value) if value else '')

    @property
    def material_name(self) -> 'str':
        """str: 'MaterialName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialName

        if temp is None:
            return None

        return temp

    @property
    def maximum_tip_diameter(self) -> 'float':
        """float: 'MaximumTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTipDiameter

        if temp is None:
            return None

        return temp

    @property
    def mean_generating_circle_diameter(self) -> 'float':
        """float: 'MeanGeneratingCircleDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanGeneratingCircleDiameter

        if temp is None:
            return None

        return temp

    @property
    def mean_normal_thickness_at_half_depth(self) -> 'float':
        """float: 'MeanNormalThicknessAtHalfDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalThicknessAtHalfDepth

        if temp is None:
            return None

        return temp

    @property
    def minimum_required_rim_thickness_by_standard_iso8140042005(self) -> 'float':
        """float: 'MinimumRequiredRimThicknessByStandardISO8140042005' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRequiredRimThicknessByStandardISO8140042005

        if temp is None:
            return None

        return temp

    @property
    def minimum_root_diameter(self) -> 'float':
        """float: 'MinimumRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRootDiameter

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
    def normal_space_width_at_root_form_diameter(self) -> 'float':
        """float: 'NormalSpaceWidthAtRootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalSpaceWidthAtRootFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness_at_tip_form_diameter_at_lower_backlash_allowance(self) -> 'float':
        """float: 'NormalThicknessAtTipFormDiameterAtLowerBacklashAllowance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtTipFormDiameterAtLowerBacklashAllowance

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness_at_tip_form_diameter_at_lower_backlash_allowance_over_normal_module(self) -> 'float':
        """float: 'NormalThicknessAtTipFormDiameterAtLowerBacklashAllowanceOverNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtTipFormDiameterAtLowerBacklashAllowanceOverNormalModule

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness_at_tip_form_diameter_at_upper_backlash_allowance(self) -> 'float':
        """float: 'NormalThicknessAtTipFormDiameterAtUpperBacklashAllowance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThicknessAtTipFormDiameterAtUpperBacklashAllowance

        if temp is None:
            return None

        return temp

    @property
    def normal_tooth_thickness_at_the_base_circle(self) -> 'float':
        """float: 'NormalToothThicknessAtTheBaseCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalToothThicknessAtTheBaseCircle

        if temp is None:
            return None

        return temp

    @property
    def number_of_teeth_unsigned(self) -> 'float':
        """float: 'NumberOfTeethUnsigned' is the original name of this property."""

        temp = self.wrapped.NumberOfTeethUnsigned

        if temp is None:
            return None

        return temp

    @number_of_teeth_unsigned.setter
    def number_of_teeth_unsigned(self, value: 'float'):
        self.wrapped.NumberOfTeethUnsigned = float(value) if value else 0.0

    @property
    def number_of_teeth_with_centre_distance_adjustment(self) -> 'int':
        """int: 'NumberOfTeethWithCentreDistanceAdjustment' is the original name of this property."""

        temp = self.wrapped.NumberOfTeethWithCentreDistanceAdjustment

        if temp is None:
            return None

        return temp

    @number_of_teeth_with_centre_distance_adjustment.setter
    def number_of_teeth_with_centre_distance_adjustment(self, value: 'int'):
        self.wrapped.NumberOfTeethWithCentreDistanceAdjustment = int(value) if value else 0

    @property
    def number_of_teeth_maintaining_ratio_calculating_normal_module(self) -> 'int':
        """int: 'NumberOfTeethMaintainingRatioCalculatingNormalModule' is the original name of this property."""

        temp = self.wrapped.NumberOfTeethMaintainingRatioCalculatingNormalModule

        if temp is None:
            return None

        return temp

    @number_of_teeth_maintaining_ratio_calculating_normal_module.setter
    def number_of_teeth_maintaining_ratio_calculating_normal_module(self, value: 'int'):
        self.wrapped.NumberOfTeethMaintainingRatioCalculatingNormalModule = int(value) if value else 0

    @property
    def number_of_teeth_with_normal_module_adjustment(self) -> 'int':
        """int: 'NumberOfTeethWithNormalModuleAdjustment' is the original name of this property."""

        temp = self.wrapped.NumberOfTeethWithNormalModuleAdjustment

        if temp is None:
            return None

        return temp

    @number_of_teeth_with_normal_module_adjustment.setter
    def number_of_teeth_with_normal_module_adjustment(self, value: 'int'):
        self.wrapped.NumberOfTeethWithNormalModuleAdjustment = int(value) if value else 0

    @property
    def permissible_linear_wear(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PermissibleLinearWear' is the original name of this property."""

        temp = self.wrapped.PermissibleLinearWear

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @permissible_linear_wear.setter
    def permissible_linear_wear(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PermissibleLinearWear = value

    @property
    def radii_of_curvature_at_tip(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadiiOfCurvatureAtTip' is the original name of this property."""

        temp = self.wrapped.RadiiOfCurvatureAtTip

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @radii_of_curvature_at_tip.setter
    def radii_of_curvature_at_tip(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RadiiOfCurvatureAtTip = value

    @property
    def radii_of_curvature_at_tip_right_flank(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadiiOfCurvatureAtTipRightFlank' is the original name of this property."""

        temp = self.wrapped.RadiiOfCurvatureAtTipRightFlank

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @radii_of_curvature_at_tip_right_flank.setter
    def radii_of_curvature_at_tip_right_flank(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RadiiOfCurvatureAtTipRightFlank = value

    @property
    def reference_diameter(self) -> 'float':
        """float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceDiameter

        if temp is None:
            return None

        return temp

    @property
    def rim_diameter(self) -> 'float':
        """float: 'RimDiameter' is the original name of this property."""

        temp = self.wrapped.RimDiameter

        if temp is None:
            return None

        return temp

    @rim_diameter.setter
    def rim_diameter(self, value: 'float'):
        self.wrapped.RimDiameter = float(value) if value else 0.0

    @property
    def rim_thickness(self) -> 'float':
        """float: 'RimThickness' is the original name of this property."""

        temp = self.wrapped.RimThickness

        if temp is None:
            return None

        return temp

    @rim_thickness.setter
    def rim_thickness(self, value: 'float'):
        self.wrapped.RimThickness = float(value) if value else 0.0

    @property
    def rim_thickness_normal_module_ratio(self) -> 'float':
        """float: 'RimThicknessNormalModuleRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RimThicknessNormalModuleRatio

        if temp is None:
            return None

        return temp

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
    def root_heat_transfer_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RootHeatTransferCoefficient' is the original name of this property."""

        temp = self.wrapped.RootHeatTransferCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @root_heat_transfer_coefficient.setter
    def root_heat_transfer_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RootHeatTransferCoefficient = value

    @property
    def rotation_angle(self) -> 'float':
        """float: 'RotationAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotationAngle

        if temp is None:
            return None

        return temp

    @property
    def signed_root_diameter(self) -> 'float':
        """float: 'SignedRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SignedRootDiameter

        if temp is None:
            return None

        return temp

    @property
    def signed_tip_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SignedTipDiameter' is the original name of this property."""

        temp = self.wrapped.SignedTipDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @signed_tip_diameter.setter
    def signed_tip_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SignedTipDiameter = value

    @property
    def specified_web_thickness(self) -> 'float':
        """float: 'SpecifiedWebThickness' is the original name of this property."""

        temp = self.wrapped.SpecifiedWebThickness

        if temp is None:
            return None

        return temp

    @specified_web_thickness.setter
    def specified_web_thickness(self, value: 'float'):
        self.wrapped.SpecifiedWebThickness = float(value) if value else 0.0

    @property
    def thermal_contact_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ThermalContactCoefficient' is the original name of this property."""

        temp = self.wrapped.ThermalContactCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @thermal_contact_coefficient.setter
    def thermal_contact_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ThermalContactCoefficient = value

    @property
    def tip_alteration_coefficient(self) -> 'float':
        """float: 'TipAlterationCoefficient' is the original name of this property."""

        temp = self.wrapped.TipAlterationCoefficient

        if temp is None:
            return None

        return temp

    @tip_alteration_coefficient.setter
    def tip_alteration_coefficient(self, value: 'float'):
        self.wrapped.TipAlterationCoefficient = float(value) if value else 0.0

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
    def tip_thickness(self) -> 'float':
        """float: 'TipThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipThickness

        if temp is None:
            return None

        return temp

    @property
    def tip_thickness_at_lower_backlash_allowance(self) -> 'float':
        """float: 'TipThicknessAtLowerBacklashAllowance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipThicknessAtLowerBacklashAllowance

        if temp is None:
            return None

        return temp

    @property
    def tip_thickness_at_lower_backlash_allowance_over_normal_module(self) -> 'float':
        """float: 'TipThicknessAtLowerBacklashAllowanceOverNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipThicknessAtLowerBacklashAllowanceOverNormalModule

        if temp is None:
            return None

        return temp

    @property
    def tip_thickness_at_upper_backlash_allowance(self) -> 'float':
        """float: 'TipThicknessAtUpperBacklashAllowance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipThicknessAtUpperBacklashAllowance

        if temp is None:
            return None

        return temp

    @property
    def tooth_depth(self) -> 'float':
        """float: 'ToothDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothDepth

        if temp is None:
            return None

        return temp

    @property
    def transverse_tooth_thickness_at_the_base_circle(self) -> 'float':
        """float: 'TransverseToothThicknessAtTheBaseCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseToothThicknessAtTheBaseCircle

        if temp is None:
            return None

        return temp

    @property
    def use_default_design_material(self) -> 'bool':
        """bool: 'UseDefaultDesignMaterial' is the original name of this property."""

        temp = self.wrapped.UseDefaultDesignMaterial

        if temp is None:
            return None

        return temp

    @use_default_design_material.setter
    def use_default_design_material(self, value: 'bool'):
        self.wrapped.UseDefaultDesignMaterial = bool(value) if value else False

    @property
    def web_centre_offset(self) -> 'float':
        """float: 'WebCentreOffset' is the original name of this property."""

        temp = self.wrapped.WebCentreOffset

        if temp is None:
            return None

        return temp

    @web_centre_offset.setter
    def web_centre_offset(self, value: 'float'):
        self.wrapped.WebCentreOffset = float(value) if value else 0.0

    @property
    def web_status(self) -> 'str':
        """str: 'WebStatus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WebStatus

        if temp is None:
            return None

        return temp

    @property
    def agma_accuracy_grade(self) -> '_1090.AGMA20151AccuracyGrades':
        """AGMA20151AccuracyGrades: 'AGMAAccuracyGrade' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AGMAAccuracyGrade

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances(self) -> '_1092.CylindricalAccuracyGrader':
        """CylindricalAccuracyGrader: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1092.CylindricalAccuracyGrader.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to CylindricalAccuracyGrader. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_agma2000_accuracy_grader(self) -> '_1088.AGMA2000AccuracyGrader':
        """AGMA2000AccuracyGrader: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1088.AGMA2000AccuracyGrader.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to AGMA2000AccuracyGrader. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_agma20151_accuracy_grader(self) -> '_1089.AGMA20151AccuracyGrader':
        """AGMA20151AccuracyGrader: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1089.AGMA20151AccuracyGrader.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to AGMA20151AccuracyGrader. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_agmaiso13282013_accuracy_grader(self) -> '_1091.AGMAISO13282013AccuracyGrader':
        """AGMAISO13282013AccuracyGrader: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1091.AGMAISO13282013AccuracyGrader.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to AGMAISO13282013AccuracyGrader. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_cylindrical_accuracy_grader_with_profile_form_and_slope(self) -> '_1093.CylindricalAccuracyGraderWithProfileFormAndSlope':
        """CylindricalAccuracyGraderWithProfileFormAndSlope: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1093.CylindricalAccuracyGraderWithProfileFormAndSlope.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to CylindricalAccuracyGraderWithProfileFormAndSlope. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_iso13282013_accuracy_grader(self) -> '_1096.ISO13282013AccuracyGrader':
        """ISO13282013AccuracyGrader: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1096.ISO13282013AccuracyGrader.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to ISO13282013AccuracyGrader. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_iso1328_accuracy_grader(self) -> '_1097.ISO1328AccuracyGrader':
        """ISO1328AccuracyGrader: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1097.ISO1328AccuracyGrader.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to ISO1328AccuracyGrader. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grade_allowances_and_tolerances_of_type_iso1328_accuracy_grader_common(self) -> '_1098.ISO1328AccuracyGraderCommon':
        """ISO1328AccuracyGraderCommon: 'AccuracyGradeAllowancesAndTolerances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradeAllowancesAndTolerances

        if temp is None:
            return None

        if _1098.ISO1328AccuracyGraderCommon.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grade_allowances_and_tolerances to ISO1328AccuracyGraderCommon. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_specified_accuracy(self) -> '_286.AccuracyGrades':
        """AccuracyGrades: 'AccuracyGradesSpecifiedAccuracy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradesSpecifiedAccuracy

        if temp is None:
            return None

        if _286.AccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades_specified_accuracy to AccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_specified_accuracy_of_type_agma20151_accuracy_grades(self) -> '_1090.AGMA20151AccuracyGrades':
        """AGMA20151AccuracyGrades: 'AccuracyGradesSpecifiedAccuracy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradesSpecifiedAccuracy

        if temp is None:
            return None

        if _1090.AGMA20151AccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades_specified_accuracy to AGMA20151AccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_specified_accuracy_of_type_cylindrical_accuracy_grades(self) -> '_1094.CylindricalAccuracyGrades':
        """CylindricalAccuracyGrades: 'AccuracyGradesSpecifiedAccuracy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradesSpecifiedAccuracy

        if temp is None:
            return None

        if _1094.CylindricalAccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades_specified_accuracy to CylindricalAccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_specified_accuracy_of_type_iso1328_accuracy_grades(self) -> '_1099.ISO1328AccuracyGrades':
        """ISO1328AccuracyGrades: 'AccuracyGradesSpecifiedAccuracy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradesSpecifiedAccuracy

        if temp is None:
            return None

        if _1099.ISO1328AccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades_specified_accuracy to ISO1328AccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_specified_accuracy_of_type_agma_gleason_conical_accuracy_grades(self) -> '_1146.AGMAGleasonConicalAccuracyGrades':
        """AGMAGleasonConicalAccuracyGrades: 'AccuracyGradesSpecifiedAccuracy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGradesSpecifiedAccuracy

        if temp is None:
            return None

        if _1146.AGMAGleasonConicalAccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades_specified_accuracy to AGMAGleasonConicalAccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def case_hardening_properties(self) -> '_964.CaseHardeningProperties':
        """CaseHardeningProperties: 'CaseHardeningProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CaseHardeningProperties

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_cutting_options(self) -> '_973.CylindricalGearCuttingOptions':
        """CylindricalGearCuttingOptions: 'CylindricalGearCuttingOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearCuttingOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_manufacturing_configuration(self) -> '_578.CylindricalGearManufacturingConfig':
        """CylindricalGearManufacturingConfig: 'CylindricalGearManufacturingConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearManufacturingConfiguration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_micro_geometry(self) -> '_1059.CylindricalGearMicroGeometry':
        """CylindricalGearMicroGeometry: 'CylindricalGearMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_set(self) -> '_990.CylindricalGearSetDesign':
        """CylindricalGearSetDesign: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSet

        if temp is None:
            return None

        if _990.CylindricalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_set to CylindricalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def finish_stock_specification(self) -> '_1006.FinishStockSpecification':
        """FinishStockSpecification: 'FinishStockSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FinishStockSpecification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def finished_tooth_thickness_specification(self) -> '_1007.FinishToothThicknessDesignSpecification':
        """FinishToothThicknessDesignSpecification: 'FinishedToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FinishedToothThicknessSpecification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso6336_geometry(self) -> '_1016.ISO6336GeometryBase':
        """ISO6336GeometryBase: 'ISO6336Geometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO6336Geometry

        if temp is None:
            return None

        if _1016.ISO6336GeometryBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso6336_geometry to ISO6336GeometryBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso6336_geometry_of_type_iso6336_geometry(self) -> '_1015.ISO6336Geometry':
        """ISO6336Geometry: 'ISO6336Geometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO6336Geometry

        if temp is None:
            return None

        if _1015.ISO6336Geometry.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso6336_geometry to ISO6336Geometry. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso6336_geometry_of_type_iso6336_geometry_for_shaped_gears(self) -> '_1017.ISO6336GeometryForShapedGears':
        """ISO6336GeometryForShapedGears: 'ISO6336Geometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO6336Geometry

        if temp is None:
            return None

        if _1017.ISO6336GeometryForShapedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso6336_geometry to ISO6336GeometryForShapedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso6336_geometry_of_type_iso6336_geometry_manufactured(self) -> '_1018.ISO6336GeometryManufactured':
        """ISO6336GeometryManufactured: 'ISO6336Geometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO6336Geometry

        if temp is None:
            return None

        if _1018.ISO6336GeometryManufactured.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast iso6336_geometry to ISO6336GeometryManufactured. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def iso_accuracy_grade(self) -> '_1099.ISO1328AccuracyGrades':
        """ISO1328AccuracyGrades: 'ISOAccuracyGrade' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOAccuracyGrade

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_flank(self) -> '_981.CylindricalGearFlankDesign':
        """CylindricalGearFlankDesign: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material(self) -> '_560.GearMaterial':
        """GearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _560.GearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to GearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_agma_cylindrical_gear_material(self) -> '_549.AGMACylindricalGearMaterial':
        """AGMACylindricalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _549.AGMACylindricalGearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to AGMACylindricalGearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_bevel_gear_iso_material(self) -> '_551.BevelGearISOMaterial':
        """BevelGearISOMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _551.BevelGearISOMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to BevelGearISOMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_bevel_gear_material(self) -> '_553.BevelGearMaterial':
        """BevelGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _553.BevelGearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to BevelGearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_cylindrical_gear_material(self) -> '_557.CylindricalGearMaterial':
        """CylindricalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _557.CylindricalGearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to CylindricalGearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_iso_cylindrical_gear_material(self) -> '_563.ISOCylindricalGearMaterial':
        """ISOCylindricalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _563.ISOCylindricalGearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to ISOCylindricalGearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_klingelnberg_cyclo_palloid_conical_gear_material(self) -> '_567.KlingelnbergCycloPalloidConicalGearMaterial':
        """KlingelnbergCycloPalloidConicalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _567.KlingelnbergCycloPalloidConicalGearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to KlingelnbergCycloPalloidConicalGearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_type_plastic_cylindrical_gear_material(self) -> '_569.PlasticCylindricalGearMaterial':
        """PlasticCylindricalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _569.PlasticCylindricalGearMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to PlasticCylindricalGearMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micro_geometry_settings(self) -> '_984.CylindricalGearMicroGeometrySettings':
        """CylindricalGearMicroGeometrySettings: 'MicroGeometrySettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicroGeometrySettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_981.CylindricalGearFlankDesign':
        """CylindricalGearFlankDesign: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rough_tooth_thickness_specification(self) -> '_1046.ToothThicknessSpecification':
        """ToothThicknessSpecification: 'RoughToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughToothThicknessSpecification

        if temp is None:
            return None

        if _1046.ToothThicknessSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rough_tooth_thickness_specification to ToothThicknessSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def surface_roughness(self) -> '_1039.SurfaceRoughness':
        """SurfaceRoughness: 'SurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceRoughness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_of_gear_fits(self) -> '_1095.DIN3967SystemOfGearFits':
        """DIN3967SystemOfGearFits: 'SystemOfGearFits' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemOfGearFits

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tiff_analysis_settings(self) -> '_1041.TiffAnalysisSettings':
        """TiffAnalysisSettings: 'TIFFAnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TIFFAnalysisSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_meshes(self) -> 'List[_982.CylindricalGearMeshDesign]':
        """List[CylindricalGearMeshDesign]: 'CylindricalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flanks(self) -> 'List[_981.CylindricalGearFlankDesign]':
        """List[CylindricalGearFlankDesign]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Flanks

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def both_flanks(self) -> '_981.CylindricalGearFlankDesign':
        """CylindricalGearFlankDesign: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BothFlanks

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def manufacturing_configurations(self) -> 'List[_578.CylindricalGearManufacturingConfig]':
        """List[CylindricalGearManufacturingConfig]: 'ManufacturingConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManufacturingConfigurations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def micro_geometries(self) -> 'List[_1059.CylindricalGearMicroGeometry]':
        """List[CylindricalGearMicroGeometry]: 'MicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicroGeometries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
