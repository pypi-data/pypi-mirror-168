"""_1062.py

CylindricalGearProfileModification
"""


from mastapy._internal import constructor
from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy.gears.micro_geometry import _548
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PROFILE_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearProfileModification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearProfileModification',)


class CylindricalGearProfileModification(_548.ProfileModification):
    """CylindricalGearProfileModification

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_PROFILE_MODIFICATION

    def __init__(self, instance_to_wrap: 'CylindricalGearProfileModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def barrelling_peak_point_diameter(self) -> 'float':
        """float: 'BarrellingPeakPointDiameter' is the original name of this property."""

        temp = self.wrapped.BarrellingPeakPointDiameter

        if temp is None:
            return None

        return temp

    @barrelling_peak_point_diameter.setter
    def barrelling_peak_point_diameter(self, value: 'float'):
        self.wrapped.BarrellingPeakPointDiameter = float(value) if value else 0.0

    @property
    def barrelling_peak_point_radius(self) -> 'float':
        """float: 'BarrellingPeakPointRadius' is the original name of this property."""

        temp = self.wrapped.BarrellingPeakPointRadius

        if temp is None:
            return None

        return temp

    @barrelling_peak_point_radius.setter
    def barrelling_peak_point_radius(self, value: 'float'):
        self.wrapped.BarrellingPeakPointRadius = float(value) if value else 0.0

    @property
    def barrelling_peak_point_roll_angle(self) -> 'float':
        """float: 'BarrellingPeakPointRollAngle' is the original name of this property."""

        temp = self.wrapped.BarrellingPeakPointRollAngle

        if temp is None:
            return None

        return temp

    @barrelling_peak_point_roll_angle.setter
    def barrelling_peak_point_roll_angle(self, value: 'float'):
        self.wrapped.BarrellingPeakPointRollAngle = float(value) if value else 0.0

    @property
    def barrelling_peak_point_roll_distance(self) -> 'float':
        """float: 'BarrellingPeakPointRollDistance' is the original name of this property."""

        temp = self.wrapped.BarrellingPeakPointRollDistance

        if temp is None:
            return None

        return temp

    @barrelling_peak_point_roll_distance.setter
    def barrelling_peak_point_roll_distance(self, value: 'float'):
        self.wrapped.BarrellingPeakPointRollDistance = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_diameter(self) -> 'float':
        """float: 'EvaluationLowerLimitDiameter' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitDiameter

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_diameter.setter
    def evaluation_lower_limit_diameter(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitDiameter = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_diameter_for_zero_root_relief(self) -> 'float':
        """float: 'EvaluationLowerLimitDiameterForZeroRootRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitDiameterForZeroRootRelief

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_diameter_for_zero_root_relief.setter
    def evaluation_lower_limit_diameter_for_zero_root_relief(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitDiameterForZeroRootRelief = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_radius(self) -> 'float':
        """float: 'EvaluationLowerLimitRadius' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitRadius

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_radius.setter
    def evaluation_lower_limit_radius(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitRadius = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_radius_for_zero_root_relief(self) -> 'float':
        """float: 'EvaluationLowerLimitRadiusForZeroRootRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitRadiusForZeroRootRelief

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_radius_for_zero_root_relief.setter
    def evaluation_lower_limit_radius_for_zero_root_relief(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitRadiusForZeroRootRelief = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_roll_angle(self) -> 'float':
        """float: 'EvaluationLowerLimitRollAngle' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitRollAngle

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_roll_angle.setter
    def evaluation_lower_limit_roll_angle(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitRollAngle = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_roll_angle_for_zero_root_relief(self) -> 'float':
        """float: 'EvaluationLowerLimitRollAngleForZeroRootRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitRollAngleForZeroRootRelief

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_roll_angle_for_zero_root_relief.setter
    def evaluation_lower_limit_roll_angle_for_zero_root_relief(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitRollAngleForZeroRootRelief = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_roll_distance(self) -> 'float':
        """float: 'EvaluationLowerLimitRollDistance' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitRollDistance

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_roll_distance.setter
    def evaluation_lower_limit_roll_distance(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitRollDistance = float(value) if value else 0.0

    @property
    def evaluation_lower_limit_roll_distance_for_zero_root_relief(self) -> 'float':
        """float: 'EvaluationLowerLimitRollDistanceForZeroRootRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitRollDistanceForZeroRootRelief

        if temp is None:
            return None

        return temp

    @evaluation_lower_limit_roll_distance_for_zero_root_relief.setter
    def evaluation_lower_limit_roll_distance_for_zero_root_relief(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitRollDistanceForZeroRootRelief = float(value) if value else 0.0

    @property
    def evaluation_of_linear_root_relief_diameter(self) -> 'float':
        """float: 'EvaluationOfLinearRootReliefDiameter' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRootReliefDiameter

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_root_relief_diameter.setter
    def evaluation_of_linear_root_relief_diameter(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRootReliefDiameter = float(value) if value else 0.0

    @property
    def evaluation_of_linear_root_relief_radius(self) -> 'float':
        """float: 'EvaluationOfLinearRootReliefRadius' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRootReliefRadius

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_root_relief_radius.setter
    def evaluation_of_linear_root_relief_radius(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRootReliefRadius = float(value) if value else 0.0

    @property
    def evaluation_of_linear_root_relief_roll_angle(self) -> 'float':
        """float: 'EvaluationOfLinearRootReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRootReliefRollAngle

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_root_relief_roll_angle.setter
    def evaluation_of_linear_root_relief_roll_angle(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRootReliefRollAngle = float(value) if value else 0.0

    @property
    def evaluation_of_linear_root_relief_roll_distance(self) -> 'float':
        """float: 'EvaluationOfLinearRootReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRootReliefRollDistance

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_root_relief_roll_distance.setter
    def evaluation_of_linear_root_relief_roll_distance(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRootReliefRollDistance = float(value) if value else 0.0

    @property
    def evaluation_of_linear_tip_relief_diameter(self) -> 'float':
        """float: 'EvaluationOfLinearTipReliefDiameter' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearTipReliefDiameter

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_tip_relief_diameter.setter
    def evaluation_of_linear_tip_relief_diameter(self, value: 'float'):
        self.wrapped.EvaluationOfLinearTipReliefDiameter = float(value) if value else 0.0

    @property
    def evaluation_of_linear_tip_relief_radius(self) -> 'float':
        """float: 'EvaluationOfLinearTipReliefRadius' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearTipReliefRadius

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_tip_relief_radius.setter
    def evaluation_of_linear_tip_relief_radius(self, value: 'float'):
        self.wrapped.EvaluationOfLinearTipReliefRadius = float(value) if value else 0.0

    @property
    def evaluation_of_linear_tip_relief_roll_angle(self) -> 'float':
        """float: 'EvaluationOfLinearTipReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearTipReliefRollAngle

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_tip_relief_roll_angle.setter
    def evaluation_of_linear_tip_relief_roll_angle(self, value: 'float'):
        self.wrapped.EvaluationOfLinearTipReliefRollAngle = float(value) if value else 0.0

    @property
    def evaluation_of_linear_tip_relief_roll_distance(self) -> 'float':
        """float: 'EvaluationOfLinearTipReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearTipReliefRollDistance

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_tip_relief_roll_distance.setter
    def evaluation_of_linear_tip_relief_roll_distance(self, value: 'float'):
        self.wrapped.EvaluationOfLinearTipReliefRollDistance = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_root_relief_diameter(self) -> 'float':
        """float: 'EvaluationOfParabolicRootReliefDiameter' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRootReliefDiameter

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_root_relief_diameter.setter
    def evaluation_of_parabolic_root_relief_diameter(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRootReliefDiameter = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_root_relief_radius(self) -> 'float':
        """float: 'EvaluationOfParabolicRootReliefRadius' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRootReliefRadius

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_root_relief_radius.setter
    def evaluation_of_parabolic_root_relief_radius(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRootReliefRadius = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_root_relief_roll_angle(self) -> 'float':
        """float: 'EvaluationOfParabolicRootReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRootReliefRollAngle

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_root_relief_roll_angle.setter
    def evaluation_of_parabolic_root_relief_roll_angle(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRootReliefRollAngle = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_root_relief_roll_distance(self) -> 'float':
        """float: 'EvaluationOfParabolicRootReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRootReliefRollDistance

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_root_relief_roll_distance.setter
    def evaluation_of_parabolic_root_relief_roll_distance(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRootReliefRollDistance = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_tip_relief_diameter(self) -> 'float':
        """float: 'EvaluationOfParabolicTipReliefDiameter' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicTipReliefDiameter

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_tip_relief_diameter.setter
    def evaluation_of_parabolic_tip_relief_diameter(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicTipReliefDiameter = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_tip_relief_radius(self) -> 'float':
        """float: 'EvaluationOfParabolicTipReliefRadius' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicTipReliefRadius

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_tip_relief_radius.setter
    def evaluation_of_parabolic_tip_relief_radius(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicTipReliefRadius = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_tip_relief_roll_angle(self) -> 'float':
        """float: 'EvaluationOfParabolicTipReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicTipReliefRollAngle

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_tip_relief_roll_angle.setter
    def evaluation_of_parabolic_tip_relief_roll_angle(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicTipReliefRollAngle = float(value) if value else 0.0

    @property
    def evaluation_of_parabolic_tip_relief_roll_distance(self) -> 'float':
        """float: 'EvaluationOfParabolicTipReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicTipReliefRollDistance

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_tip_relief_roll_distance.setter
    def evaluation_of_parabolic_tip_relief_roll_distance(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicTipReliefRollDistance = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_diameter(self) -> 'float':
        """float: 'EvaluationUpperLimitDiameter' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitDiameter

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_diameter.setter
    def evaluation_upper_limit_diameter(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitDiameter = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_diameter_for_zero_tip_relief(self) -> 'float':
        """float: 'EvaluationUpperLimitDiameterForZeroTipRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitDiameterForZeroTipRelief

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_diameter_for_zero_tip_relief.setter
    def evaluation_upper_limit_diameter_for_zero_tip_relief(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitDiameterForZeroTipRelief = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_radius(self) -> 'float':
        """float: 'EvaluationUpperLimitRadius' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitRadius

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_radius.setter
    def evaluation_upper_limit_radius(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitRadius = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_radius_for_zero_tip_relief(self) -> 'float':
        """float: 'EvaluationUpperLimitRadiusForZeroTipRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitRadiusForZeroTipRelief

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_radius_for_zero_tip_relief.setter
    def evaluation_upper_limit_radius_for_zero_tip_relief(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitRadiusForZeroTipRelief = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_roll_angle(self) -> 'float':
        """float: 'EvaluationUpperLimitRollAngle' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitRollAngle

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_roll_angle.setter
    def evaluation_upper_limit_roll_angle(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitRollAngle = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_roll_angle_for_zero_tip_relief(self) -> 'float':
        """float: 'EvaluationUpperLimitRollAngleForZeroTipRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitRollAngleForZeroTipRelief

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_roll_angle_for_zero_tip_relief.setter
    def evaluation_upper_limit_roll_angle_for_zero_tip_relief(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitRollAngleForZeroTipRelief = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_roll_distance(self) -> 'float':
        """float: 'EvaluationUpperLimitRollDistance' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitRollDistance

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_roll_distance.setter
    def evaluation_upper_limit_roll_distance(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitRollDistance = float(value) if value else 0.0

    @property
    def evaluation_upper_limit_roll_distance_for_zero_tip_relief(self) -> 'float':
        """float: 'EvaluationUpperLimitRollDistanceForZeroTipRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitRollDistanceForZeroTipRelief

        if temp is None:
            return None

        return temp

    @evaluation_upper_limit_roll_distance_for_zero_tip_relief.setter
    def evaluation_upper_limit_roll_distance_for_zero_tip_relief(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitRollDistanceForZeroTipRelief = float(value) if value else 0.0

    @property
    def linear_relief_isoagmadin(self) -> 'float':
        """float: 'LinearReliefISOAGMADIN' is the original name of this property."""

        temp = self.wrapped.LinearReliefISOAGMADIN

        if temp is None:
            return None

        return temp

    @linear_relief_isoagmadin.setter
    def linear_relief_isoagmadin(self, value: 'float'):
        self.wrapped.LinearReliefISOAGMADIN = float(value) if value else 0.0

    @property
    def linear_relief_ldp(self) -> 'float':
        """float: 'LinearReliefLDP' is the original name of this property."""

        temp = self.wrapped.LinearReliefLDP

        if temp is None:
            return None

        return temp

    @linear_relief_ldp.setter
    def linear_relief_ldp(self, value: 'float'):
        self.wrapped.LinearReliefLDP = float(value) if value else 0.0

    @property
    def linear_relief_vdi(self) -> 'float':
        """float: 'LinearReliefVDI' is the original name of this property."""

        temp = self.wrapped.LinearReliefVDI

        if temp is None:
            return None

        return temp

    @linear_relief_vdi.setter
    def linear_relief_vdi(self, value: 'float'):
        self.wrapped.LinearReliefVDI = float(value) if value else 0.0

    @property
    def pressure_angle_modification(self) -> 'float':
        """float: 'PressureAngleModification' is the original name of this property."""

        temp = self.wrapped.PressureAngleModification

        if temp is None:
            return None

        return temp

    @pressure_angle_modification.setter
    def pressure_angle_modification(self, value: 'float'):
        self.wrapped.PressureAngleModification = float(value) if value else 0.0

    @property
    def profile_modification_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'ProfileModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileModificationChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast profile_modification_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def start_of_linear_root_relief_diameter(self) -> 'float':
        """float: 'StartOfLinearRootReliefDiameter' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRootReliefDiameter

        if temp is None:
            return None

        return temp

    @start_of_linear_root_relief_diameter.setter
    def start_of_linear_root_relief_diameter(self, value: 'float'):
        self.wrapped.StartOfLinearRootReliefDiameter = float(value) if value else 0.0

    @property
    def start_of_linear_root_relief_radius(self) -> 'float':
        """float: 'StartOfLinearRootReliefRadius' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRootReliefRadius

        if temp is None:
            return None

        return temp

    @start_of_linear_root_relief_radius.setter
    def start_of_linear_root_relief_radius(self, value: 'float'):
        self.wrapped.StartOfLinearRootReliefRadius = float(value) if value else 0.0

    @property
    def start_of_linear_root_relief_roll_angle(self) -> 'float':
        """float: 'StartOfLinearRootReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRootReliefRollAngle

        if temp is None:
            return None

        return temp

    @start_of_linear_root_relief_roll_angle.setter
    def start_of_linear_root_relief_roll_angle(self, value: 'float'):
        self.wrapped.StartOfLinearRootReliefRollAngle = float(value) if value else 0.0

    @property
    def start_of_linear_root_relief_roll_distance(self) -> 'float':
        """float: 'StartOfLinearRootReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRootReliefRollDistance

        if temp is None:
            return None

        return temp

    @start_of_linear_root_relief_roll_distance.setter
    def start_of_linear_root_relief_roll_distance(self, value: 'float'):
        self.wrapped.StartOfLinearRootReliefRollDistance = float(value) if value else 0.0

    @property
    def start_of_linear_tip_relief_diameter(self) -> 'float':
        """float: 'StartOfLinearTipReliefDiameter' is the original name of this property."""

        temp = self.wrapped.StartOfLinearTipReliefDiameter

        if temp is None:
            return None

        return temp

    @start_of_linear_tip_relief_diameter.setter
    def start_of_linear_tip_relief_diameter(self, value: 'float'):
        self.wrapped.StartOfLinearTipReliefDiameter = float(value) if value else 0.0

    @property
    def start_of_linear_tip_relief_radius(self) -> 'float':
        """float: 'StartOfLinearTipReliefRadius' is the original name of this property."""

        temp = self.wrapped.StartOfLinearTipReliefRadius

        if temp is None:
            return None

        return temp

    @start_of_linear_tip_relief_radius.setter
    def start_of_linear_tip_relief_radius(self, value: 'float'):
        self.wrapped.StartOfLinearTipReliefRadius = float(value) if value else 0.0

    @property
    def start_of_linear_tip_relief_roll_angle(self) -> 'float':
        """float: 'StartOfLinearTipReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.StartOfLinearTipReliefRollAngle

        if temp is None:
            return None

        return temp

    @start_of_linear_tip_relief_roll_angle.setter
    def start_of_linear_tip_relief_roll_angle(self, value: 'float'):
        self.wrapped.StartOfLinearTipReliefRollAngle = float(value) if value else 0.0

    @property
    def start_of_linear_tip_relief_roll_distance(self) -> 'float':
        """float: 'StartOfLinearTipReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.StartOfLinearTipReliefRollDistance

        if temp is None:
            return None

        return temp

    @start_of_linear_tip_relief_roll_distance.setter
    def start_of_linear_tip_relief_roll_distance(self, value: 'float'):
        self.wrapped.StartOfLinearTipReliefRollDistance = float(value) if value else 0.0

    @property
    def start_of_parabolic_root_relief_diameter(self) -> 'float':
        """float: 'StartOfParabolicRootReliefDiameter' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRootReliefDiameter

        if temp is None:
            return None

        return temp

    @start_of_parabolic_root_relief_diameter.setter
    def start_of_parabolic_root_relief_diameter(self, value: 'float'):
        self.wrapped.StartOfParabolicRootReliefDiameter = float(value) if value else 0.0

    @property
    def start_of_parabolic_root_relief_radius(self) -> 'float':
        """float: 'StartOfParabolicRootReliefRadius' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRootReliefRadius

        if temp is None:
            return None

        return temp

    @start_of_parabolic_root_relief_radius.setter
    def start_of_parabolic_root_relief_radius(self, value: 'float'):
        self.wrapped.StartOfParabolicRootReliefRadius = float(value) if value else 0.0

    @property
    def start_of_parabolic_root_relief_roll_angle(self) -> 'float':
        """float: 'StartOfParabolicRootReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRootReliefRollAngle

        if temp is None:
            return None

        return temp

    @start_of_parabolic_root_relief_roll_angle.setter
    def start_of_parabolic_root_relief_roll_angle(self, value: 'float'):
        self.wrapped.StartOfParabolicRootReliefRollAngle = float(value) if value else 0.0

    @property
    def start_of_parabolic_root_relief_roll_distance(self) -> 'float':
        """float: 'StartOfParabolicRootReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRootReliefRollDistance

        if temp is None:
            return None

        return temp

    @start_of_parabolic_root_relief_roll_distance.setter
    def start_of_parabolic_root_relief_roll_distance(self, value: 'float'):
        self.wrapped.StartOfParabolicRootReliefRollDistance = float(value) if value else 0.0

    @property
    def start_of_parabolic_tip_relief_diameter(self) -> 'float':
        """float: 'StartOfParabolicTipReliefDiameter' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicTipReliefDiameter

        if temp is None:
            return None

        return temp

    @start_of_parabolic_tip_relief_diameter.setter
    def start_of_parabolic_tip_relief_diameter(self, value: 'float'):
        self.wrapped.StartOfParabolicTipReliefDiameter = float(value) if value else 0.0

    @property
    def start_of_parabolic_tip_relief_radius(self) -> 'float':
        """float: 'StartOfParabolicTipReliefRadius' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicTipReliefRadius

        if temp is None:
            return None

        return temp

    @start_of_parabolic_tip_relief_radius.setter
    def start_of_parabolic_tip_relief_radius(self, value: 'float'):
        self.wrapped.StartOfParabolicTipReliefRadius = float(value) if value else 0.0

    @property
    def start_of_parabolic_tip_relief_roll_angle(self) -> 'float':
        """float: 'StartOfParabolicTipReliefRollAngle' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicTipReliefRollAngle

        if temp is None:
            return None

        return temp

    @start_of_parabolic_tip_relief_roll_angle.setter
    def start_of_parabolic_tip_relief_roll_angle(self, value: 'float'):
        self.wrapped.StartOfParabolicTipReliefRollAngle = float(value) if value else 0.0

    @property
    def start_of_parabolic_tip_relief_roll_distance(self) -> 'float':
        """float: 'StartOfParabolicTipReliefRollDistance' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicTipReliefRollDistance

        if temp is None:
            return None

        return temp

    @start_of_parabolic_tip_relief_roll_distance.setter
    def start_of_parabolic_tip_relief_roll_distance(self, value: 'float'):
        self.wrapped.StartOfParabolicTipReliefRollDistance = float(value) if value else 0.0

    @property
    def barrelling_peak_point(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'BarrellingPeakPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BarrellingPeakPoint

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def evaluation_lower_limit(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'EvaluationLowerLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EvaluationLowerLimit

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def evaluation_lower_limit_for_zero_root_relief(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'EvaluationLowerLimitForZeroRootRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EvaluationLowerLimitForZeroRootRelief

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def evaluation_upper_limit(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'EvaluationUpperLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EvaluationUpperLimit

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def evaluation_upper_limit_for_zero_tip_relief(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'EvaluationUpperLimitForZeroTipRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EvaluationUpperLimitForZeroTipRelief

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_root_relief_evaluation(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LinearRootReliefEvaluation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearRootReliefEvaluation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_root_relief_start(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LinearRootReliefStart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearRootReliefStart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_tip_relief_evaluation(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LinearTipReliefEvaluation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearTipReliefEvaluation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_tip_relief_start(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'LinearTipReliefStart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearTipReliefStart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parabolic_root_relief_evaluation(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ParabolicRootReliefEvaluation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParabolicRootReliefEvaluation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parabolic_root_relief_start(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ParabolicRootReliefStart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParabolicRootReliefStart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parabolic_tip_relief_evaluation(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ParabolicTipReliefEvaluation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParabolicTipReliefEvaluation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parabolic_tip_relief_start(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ParabolicTipReliefStart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParabolicTipReliefStart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def relief_of(self, roll_distance: 'float') -> 'float':
        """ 'ReliefOf' is the original name of this method.

        Args:
            roll_distance (float)

        Returns:
            float
        """

        roll_distance = float(roll_distance)
        method_result = self.wrapped.ReliefOf(roll_distance if roll_distance else 0.0)
        return method_result
