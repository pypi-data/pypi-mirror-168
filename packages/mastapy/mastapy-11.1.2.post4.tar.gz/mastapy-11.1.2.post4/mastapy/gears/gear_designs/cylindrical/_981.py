"""_981.py

CylindricalGearFlankDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FLANK_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearFlankDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFlankDesign',)


class CylindricalGearFlankDesign(_0.APIBase):
    """CylindricalGearFlankDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FLANK_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearFlankDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_base_diameter(self) -> 'float':
        """float: 'AbsoluteBaseDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteBaseDiameter

        if temp is None:
            return None

        return temp

    @property
    def absolute_form_diameter(self) -> 'float':
        """float: 'AbsoluteFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def absolute_form_to_sap_diameter_clearance(self) -> 'float':
        """float: 'AbsoluteFormToSAPDiameterClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteFormToSAPDiameterClearance

        if temp is None:
            return None

        return temp

    @property
    def absolute_tip_form_diameter(self) -> 'float':
        """float: 'AbsoluteTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AbsoluteTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def base_diameter(self) -> 'float':
        """float: 'BaseDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseDiameter

        if temp is None:
            return None

        return temp

    @property
    def base_thickness_half_angle(self) -> 'float':
        """float: 'BaseThicknessHalfAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseThicknessHalfAngle

        if temp is None:
            return None

        return temp

    @property
    def base_to_form_diameter_clearance(self) -> 'float':
        """float: 'BaseToFormDiameterClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseToFormDiameterClearance

        if temp is None:
            return None

        return temp

    @property
    def base_to_form_diameter_clearance_as_normal_module_ratio(self) -> 'float':
        """float: 'BaseToFormDiameterClearanceAsNormalModuleRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseToFormDiameterClearanceAsNormalModuleRatio

        if temp is None:
            return None

        return temp

    @property
    def chamfer_angle_in_normal_plane(self) -> 'float':
        """float: 'ChamferAngleInNormalPlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChamferAngleInNormalPlane

        if temp is None:
            return None

        return temp

    @property
    def effective_tip_radius(self) -> 'float':
        """float: 'EffectiveTipRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveTipRadius

        if temp is None:
            return None

        return temp

    @property
    def flank_name(self) -> 'str':
        """str: 'FlankName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlankName

        if temp is None:
            return None

        return temp

    @property
    def form_radius(self) -> 'float':
        """float: 'FormRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormRadius

        if temp is None:
            return None

        return temp

    @property
    def form_to_sap_diameter_absolute_clearance_as_normal_module_ratio(self) -> 'float':
        """float: 'FormToSAPDiameterAbsoluteClearanceAsNormalModuleRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormToSAPDiameterAbsoluteClearanceAsNormalModuleRatio

        if temp is None:
            return None

        return temp

    @property
    def has_chamfer(self) -> 'bool':
        """bool: 'HasChamfer' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasChamfer

        if temp is None:
            return None

        return temp

    @property
    def lowest_sap_diameter(self) -> 'float':
        """float: 'LowestSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LowestSAPDiameter

        if temp is None:
            return None

        return temp

    @property
    def mean_normal_thickness_at_root_form_diameter(self) -> 'float':
        """float: 'MeanNormalThicknessAtRootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalThicknessAtRootFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def mean_normal_thickness_at_tip_form_diameter(self) -> 'float':
        """float: 'MeanNormalThicknessAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalThicknessAtTipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def normal_base_pitch(self) -> 'float':
        """float: 'NormalBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalBasePitch

        if temp is None:
            return None

        return temp

    @property
    def normal_pressure_angle(self) -> 'float':
        """float: 'NormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def root_form_diameter(self) -> 'float':
        """float: 'RootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def root_form_roll_angle(self) -> 'float':
        """float: 'RootFormRollAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFormRollAngle

        if temp is None:
            return None

        return temp

    @property
    def root_form_roll_distance(self) -> 'float':
        """float: 'RootFormRollDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFormRollDistance

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
    def tip_form_diameter(self) -> 'float':
        """float: 'TipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipFormDiameter

        if temp is None:
            return None

        return temp

    @property
    def tip_form_roll_angle(self) -> 'float':
        """float: 'TipFormRollAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipFormRollAngle

        if temp is None:
            return None

        return temp

    @property
    def tip_form_roll_distance(self) -> 'float':
        """float: 'TipFormRollDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipFormRollDistance

        if temp is None:
            return None

        return temp

    @property
    def tooth_thickness_half_angle_at_reference_circle(self) -> 'float':
        """float: 'ToothThicknessHalfAngleAtReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessHalfAngleAtReferenceCircle

        if temp is None:
            return None

        return temp

    @property
    def transverse_base_pitch(self) -> 'float':
        """float: 'TransverseBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseBasePitch

        if temp is None:
            return None

        return temp

    @property
    def transverse_chamfer_angle(self) -> 'float':
        """float: 'TransverseChamferAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseChamferAngle

        if temp is None:
            return None

        return temp

    @property
    def transverse_pressure_angle(self) -> 'float':
        """float: 'TransversePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransversePressureAngle

        if temp is None:
            return None

        return temp

    @property
    def highest_point_of_fewest_tooth_contacts(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'HighestPointOfFewestToothContacts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HighestPointOfFewestToothContacts

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lowest_point_of_fewest_tooth_contacts(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LowestPointOfFewestToothContacts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LowestPointOfFewestToothContacts

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lowest_start_of_active_profile(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LowestStartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LowestStartOfActiveProfile

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def root_diameter_reporting(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'RootDiameterReporting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootDiameterReporting

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def root_form(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'RootForm' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootForm

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tip_diameter_reporting(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'TipDiameterReporting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipDiameterReporting

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tip_form(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'TipForm' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipForm

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
