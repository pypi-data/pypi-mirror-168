"""_950.py

HypoidGearSetDesign
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.hypoid import _948, _949
from mastapy.gears.gear_designs.agma_gleason_conical import _1149
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Hypoid', 'HypoidGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetDesign',)


class HypoidGearSetDesign(_1149.AGMAGleasonConicalGearSetDesign):
    """HypoidGearSetDesign

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'HypoidGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_pressure_angle(self) -> 'float':
        """float: 'AveragePressureAngle' is the original name of this property."""

        temp = self.wrapped.AveragePressureAngle

        if temp is None:
            return None

        return temp

    @average_pressure_angle.setter
    def average_pressure_angle(self, value: 'float'):
        self.wrapped.AveragePressureAngle = float(value) if value else 0.0

    @property
    def backlash_allowance_max(self) -> 'float':
        """float: 'BacklashAllowanceMax' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BacklashAllowanceMax

        if temp is None:
            return None

        return temp

    @property
    def backlash_allowance_min(self) -> 'float':
        """float: 'BacklashAllowanceMin' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BacklashAllowanceMin

        if temp is None:
            return None

        return temp

    @property
    def basic_crown_gear_addendum_factor(self) -> 'float':
        """float: 'BasicCrownGearAddendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicCrownGearAddendumFactor

        if temp is None:
            return None

        return temp

    @property
    def basic_crown_gear_dedendum_factor(self) -> 'float':
        """float: 'BasicCrownGearDedendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicCrownGearDedendumFactor

        if temp is None:
            return None

        return temp

    @property
    def clearance(self) -> 'float':
        """float: 'Clearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clearance

        if temp is None:
            return None

        return temp

    @property
    def depth_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DepthFactor' is the original name of this property."""

        temp = self.wrapped.DepthFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @depth_factor.setter
    def depth_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DepthFactor = value

    @property
    def desired_pinion_spiral_angle(self) -> 'float':
        """float: 'DesiredPinionSpiralAngle' is the original name of this property."""

        temp = self.wrapped.DesiredPinionSpiralAngle

        if temp is None:
            return None

        return temp

    @desired_pinion_spiral_angle.setter
    def desired_pinion_spiral_angle(self, value: 'float'):
        self.wrapped.DesiredPinionSpiralAngle = float(value) if value else 0.0

    @property
    def diametral_pitch(self) -> 'float':
        """float: 'DiametralPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiametralPitch

        if temp is None:
            return None

        return temp

    @property
    def distance_from_midpoint_of_tooth(self) -> 'float':
        """float: 'DistanceFromMidpointOfTooth' is the original name of this property."""

        temp = self.wrapped.DistanceFromMidpointOfTooth

        if temp is None:
            return None

        return temp

    @distance_from_midpoint_of_tooth.setter
    def distance_from_midpoint_of_tooth(self, value: 'float'):
        self.wrapped.DistanceFromMidpointOfTooth = float(value) if value else 0.0

    @property
    def elastic_coefficient(self) -> 'float':
        """float: 'ElasticCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticCoefficient

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
    def geometry_factor_i(self) -> 'float':
        """float: 'GeometryFactorI' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorI

        if temp is None:
            return None

        return temp

    @property
    def hardness_ratio_factor(self) -> 'float':
        """float: 'HardnessRatioFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HardnessRatioFactor

        if temp is None:
            return None

        return temp

    @property
    def influence_factor_of_limit_pressure_angle(self) -> 'float':
        """float: 'InfluenceFactorOfLimitPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InfluenceFactorOfLimitPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def limit_pressure_angle(self) -> 'float':
        """float: 'LimitPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def mean_circular_pitch(self) -> 'float':
        """float: 'MeanCircularPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCircularPitch

        if temp is None:
            return None

        return temp

    @property
    def mean_clearance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MeanClearanceFactor' is the original name of this property."""

        temp = self.wrapped.MeanClearanceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @mean_clearance_factor.setter
    def mean_clearance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MeanClearanceFactor = value

    @property
    def mean_diametral_pitch(self) -> 'float':
        """float: 'MeanDiametralPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanDiametralPitch

        if temp is None:
            return None

        return temp

    @property
    def modified_contact_ratio(self) -> 'float':
        """float: 'ModifiedContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedContactRatio

        if temp is None:
            return None

        return temp

    @property
    def offset(self) -> 'float':
        """float: 'Offset' is the original name of this property."""

        temp = self.wrapped.Offset

        if temp is None:
            return None

        return temp

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value else 0.0

    @property
    def pinion_concave_root_pressure_angle(self) -> 'float':
        """float: 'PinionConcaveRootPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionConcaveRootPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_convex_root_pressure_angle(self) -> 'float':
        """float: 'PinionConvexRootPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionConvexRootPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_face_angle(self) -> 'float':
        """float: 'PinionFaceAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionFaceAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_inner_dedendum(self) -> 'float':
        """float: 'PinionInnerDedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionInnerDedendum

        if temp is None:
            return None

        return temp

    @property
    def pinion_inner_dedendum_limit(self) -> 'float':
        """float: 'PinionInnerDedendumLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionInnerDedendumLimit

        if temp is None:
            return None

        return temp

    @property
    def pinion_inner_spiral_angle(self) -> 'float':
        """float: 'PinionInnerSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionInnerSpiralAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_mean_pitch_concave_pressure_angle(self) -> 'float':
        """float: 'PinionMeanPitchConcavePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionMeanPitchConcavePressureAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_mean_pitch_convex_pressure_angle(self) -> 'float':
        """float: 'PinionMeanPitchConvexPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionMeanPitchConvexPressureAngle

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
    def pinion_offset_angle_in_pitch_plane_at_inner_end(self) -> 'float':
        """float: 'PinionOffsetAngleInPitchPlaneAtInnerEnd' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionOffsetAngleInPitchPlaneAtInnerEnd

        if temp is None:
            return None

        return temp

    @property
    def pinion_offset_angle_in_pitch_plane(self) -> 'float':
        """float: 'PinionOffsetAngleInPitchPlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionOffsetAngleInPitchPlane

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
    def pinion_passed_undercut_check(self) -> 'bool':
        """bool: 'PinionPassedUndercutCheck' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionPassedUndercutCheck

        if temp is None:
            return None

        return temp

    @property
    def pinion_pitch_angle(self) -> 'float':
        """float: 'PinionPitchAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionPitchAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_root_angle(self) -> 'float':
        """float: 'PinionRootAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionRootAngle

        if temp is None:
            return None

        return temp

    @property
    def pinion_thickness_modification_coefficient_backlash_included(self) -> 'float':
        """float: 'PinionThicknessModificationCoefficientBacklashIncluded' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionThicknessModificationCoefficientBacklashIncluded

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
    def profile_contact_ratio(self) -> 'float':
        """float: 'ProfileContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileContactRatio

        if temp is None:
            return None

        return temp

    @property
    def profile_shift_coefficient(self) -> 'float':
        """float: 'ProfileShiftCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileShiftCoefficient

        if temp is None:
            return None

        return temp

    @property
    def ratio_between_offset_and_wheel_pitch_diameter(self) -> 'float':
        """float: 'RatioBetweenOffsetAndWheelPitchDiameter' is the original name of this property."""

        temp = self.wrapped.RatioBetweenOffsetAndWheelPitchDiameter

        if temp is None:
            return None

        return temp

    @ratio_between_offset_and_wheel_pitch_diameter.setter
    def ratio_between_offset_and_wheel_pitch_diameter(self, value: 'float'):
        self.wrapped.RatioBetweenOffsetAndWheelPitchDiameter = float(value) if value else 0.0

    @property
    def rough_cutter_point_width(self) -> 'float':
        """float: 'RoughCutterPointWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughCutterPointWidth

        if temp is None:
            return None

        return temp

    @property
    def shaft_angle_departure_from_perpendicular(self) -> 'float':
        """float: 'ShaftAngleDepartureFromPerpendicular' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftAngleDepartureFromPerpendicular

        if temp is None:
            return None

        return temp

    @property
    def size_factor_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SizeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def specified_wheel_addendum_angle(self) -> 'float':
        """float: 'SpecifiedWheelAddendumAngle' is the original name of this property."""

        temp = self.wrapped.SpecifiedWheelAddendumAngle

        if temp is None:
            return None

        return temp

    @specified_wheel_addendum_angle.setter
    def specified_wheel_addendum_angle(self, value: 'float'):
        self.wrapped.SpecifiedWheelAddendumAngle = float(value) if value else 0.0

    @property
    def specified_wheel_dedendum_angle(self) -> 'float':
        """float: 'SpecifiedWheelDedendumAngle' is the original name of this property."""

        temp = self.wrapped.SpecifiedWheelDedendumAngle

        if temp is None:
            return None

        return temp

    @specified_wheel_dedendum_angle.setter
    def specified_wheel_dedendum_angle(self, value: 'float'):
        self.wrapped.SpecifiedWheelDedendumAngle = float(value) if value else 0.0

    @property
    def stock_allowance(self) -> 'float':
        """float: 'StockAllowance' is the original name of this property."""

        temp = self.wrapped.StockAllowance

        if temp is None:
            return None

        return temp

    @stock_allowance.setter
    def stock_allowance(self, value: 'float'):
        self.wrapped.StockAllowance = float(value) if value else 0.0

    @property
    def strength_balance_obtained(self) -> 'float':
        """float: 'StrengthBalanceObtained' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrengthBalanceObtained

        if temp is None:
            return None

        return temp

    @property
    def thickness_modification_coefficient_theoretical(self) -> 'float':
        """float: 'ThicknessModificationCoefficientTheoretical' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThicknessModificationCoefficientTheoretical

        if temp is None:
            return None

        return temp

    @property
    def tooth_thickness_factor(self) -> 'float':
        """float: 'ToothThicknessFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothThicknessFactor

        if temp is None:
            return None

        return temp

    @property
    def total_number_of_teeth(self) -> 'int':
        """int: 'TotalNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalNumberOfTeeth

        if temp is None:
            return None

        return temp

    @property
    def wheel_addendum_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'WheelAddendumFactor' is the original name of this property."""

        temp = self.wrapped.WheelAddendumFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @wheel_addendum_factor.setter
    def wheel_addendum_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WheelAddendumFactor = value

    @property
    def wheel_face_angle(self) -> 'float':
        """float: 'WheelFaceAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelFaceAngle

        if temp is None:
            return None

        return temp

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
    def wheel_finish_cutter_point_width(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'WheelFinishCutterPointWidth' is the original name of this property."""

        temp = self.wrapped.WheelFinishCutterPointWidth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @wheel_finish_cutter_point_width.setter
    def wheel_finish_cutter_point_width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WheelFinishCutterPointWidth = value

    @property
    def wheel_finish_cutter_point_width_suppressed(self) -> 'float':
        """float: 'WheelFinishCutterPointWidthSuppressed' is the original name of this property."""

        temp = self.wrapped.WheelFinishCutterPointWidthSuppressed

        if temp is None:
            return None

        return temp

    @wheel_finish_cutter_point_width_suppressed.setter
    def wheel_finish_cutter_point_width_suppressed(self, value: 'float'):
        self.wrapped.WheelFinishCutterPointWidthSuppressed = float(value) if value else 0.0

    @property
    def wheel_inner_blade_angle_convex(self) -> 'float':
        """float: 'WheelInnerBladeAngleConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInnerBladeAngleConvex

        if temp is None:
            return None

        return temp

    @property
    def wheel_inner_cone_distance(self) -> 'float':
        """float: 'WheelInnerConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInnerConeDistance

        if temp is None:
            return None

        return temp

    @property
    def wheel_inner_pitch_radius(self) -> 'float':
        """float: 'WheelInnerPitchRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInnerPitchRadius

        if temp is None:
            return None

        return temp

    @property
    def wheel_inner_spiral_angle(self) -> 'float':
        """float: 'WheelInnerSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInnerSpiralAngle

        if temp is None:
            return None

        return temp

    @property
    def wheel_inside_point_to_cross_point_along_wheel_axis(self) -> 'float':
        """float: 'WheelInsidePointToCrossPointAlongWheelAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInsidePointToCrossPointAlongWheelAxis

        if temp is None:
            return None

        return temp

    @property
    def wheel_mean_whole_depth(self) -> 'float':
        """float: 'WheelMeanWholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelMeanWholeDepth

        if temp is None:
            return None

        return temp

    @property
    def wheel_mean_working_depth(self) -> 'float':
        """float: 'WheelMeanWorkingDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelMeanWorkingDepth

        if temp is None:
            return None

        return temp

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
    def wheel_outer_blade_angle_concave(self) -> 'float':
        """float: 'WheelOuterBladeAngleConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelOuterBladeAngleConcave

        if temp is None:
            return None

        return temp

    @property
    def wheel_outer_spiral_angle(self) -> 'float':
        """float: 'WheelOuterSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelOuterSpiralAngle

        if temp is None:
            return None

        return temp

    @property
    def wheel_pitch_angle(self) -> 'float':
        """float: 'WheelPitchAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelPitchAngle

        if temp is None:
            return None

        return temp

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
    def wheel_root_angle(self) -> 'float':
        """float: 'WheelRootAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelRootAngle

        if temp is None:
            return None

        return temp

    @property
    def wheel_thickness_modification_coefficient_backlash_included(self) -> 'float':
        """float: 'WheelThicknessModificationCoefficientBacklashIncluded' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelThicknessModificationCoefficientBacklashIncluded

        if temp is None:
            return None

        return temp

    @property
    def wheel_whole_depth(self) -> 'float':
        """float: 'WheelWholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelWholeDepth

        if temp is None:
            return None

        return temp

    @property
    def wheel_working_depth(self) -> 'float':
        """float: 'WheelWorkingDepth' is the original name of this property."""

        temp = self.wrapped.WheelWorkingDepth

        if temp is None:
            return None

        return temp

    @wheel_working_depth.setter
    def wheel_working_depth(self, value: 'float'):
        self.wrapped.WheelWorkingDepth = float(value) if value else 0.0

    @property
    def gears(self) -> 'List[_948.HypoidGearDesign]':
        """List[HypoidGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gears(self) -> 'List[_948.HypoidGearDesign]':
        """List[HypoidGearDesign]: 'HypoidGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshes(self) -> 'List[_949.HypoidGearMeshDesign]':
        """List[HypoidGearMeshDesign]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Meshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshes(self) -> 'List[_949.HypoidGearMeshDesign]':
        """List[HypoidGearMeshDesign]: 'HypoidMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
