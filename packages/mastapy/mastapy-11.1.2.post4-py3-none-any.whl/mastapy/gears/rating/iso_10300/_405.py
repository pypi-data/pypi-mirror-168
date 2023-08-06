"""_405.py

ISO10300SingleFlankRatingMethodB2
"""


from mastapy._internal import constructor
from mastapy.gears.rating.iso_10300 import _401
from mastapy.gears.rating.virtual_cylindrical_gears import _363
from mastapy._internal.python_net import python_net_import

_ISO10300_SINGLE_FLANK_RATING_METHOD_B2 = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'ISO10300SingleFlankRatingMethodB2')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO10300SingleFlankRatingMethodB2',)


class ISO10300SingleFlankRatingMethodB2(_401.ISO10300SingleFlankRating['_363.VirtualCylindricalGearISO10300MethodB2']):
    """ISO10300SingleFlankRatingMethodB2

    This is a mastapy class.
    """

    TYPE = _ISO10300_SINGLE_FLANK_RATING_METHOD_B2

    def __init__(self, instance_to_wrap: 'ISO10300SingleFlankRatingMethodB2.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def combined_geometry_factor(self) -> 'float':
        """float: 'CombinedGeometryFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CombinedGeometryFactor

        if temp is None:
            return None

        return temp

    @property
    def contact_stress_adjustment_factor(self) -> 'float':
        """float: 'ContactStressAdjustmentFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressAdjustmentFactor

        if temp is None:
            return None

        return temp

    @property
    def cos_pressure_angle_at_point_of_load_application(self) -> 'float':
        """float: 'CosPressureAngleAtPointOfLoadApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CosPressureAngleAtPointOfLoadApplication

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
    def geometry_factor(self) -> 'float':
        """float: 'GeometryFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactor

        if temp is None:
            return None

        return temp

    @property
    def heel_increment(self) -> 'float':
        """float: 'HeelIncrement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeelIncrement

        if temp is None:
            return None

        return temp

    @property
    def heel_increment_delta_be(self) -> 'float':
        """float: 'HeelIncrementDeltaBe' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeelIncrementDeltaBe

        if temp is None:
            return None

        return temp

    @property
    def inertia_factor(self) -> 'float':
        """float: 'InertiaFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InertiaFactor

        if temp is None:
            return None

        return temp

    @property
    def L(self) -> 'float':
        """float: 'L' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.L

        if temp is None:
            return None

        return temp

    @property
    def m(self) -> 'float':
        """float: 'M' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.M

        if temp is None:
            return None

        return temp

    @property
    def nominal_value_of_root_stress_method_b2(self) -> 'float':
        """float: 'NominalValueOfRootStressMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalValueOfRootStressMethodB2

        if temp is None:
            return None

        return temp

    @property
    def o(self) -> 'float':
        """float: 'O' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.O

        if temp is None:
            return None

        return temp

    @property
    def permissible_contact_stress_method_b2(self) -> 'float':
        """float: 'PermissibleContactStressMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleContactStressMethodB2

        if temp is None:
            return None

        return temp

    @property
    def permissible_tooth_root_stress_method_b2(self) -> 'float':
        """float: 'PermissibleToothRootStressMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleToothRootStressMethodB2

        if temp is None:
            return None

        return temp

    @property
    def pressure_angle_at_point_of_load_application(self) -> 'float':
        """float: 'PressureAngleAtPointOfLoadApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureAngleAtPointOfLoadApplication

        if temp is None:
            return None

        return temp

    @property
    def projected_length_of_the_instantaneous_contact_line_in_the_tooth_lengthwise_direction(self) -> 'float':
        """float: 'ProjectedLengthOfTheInstantaneousContactLineInTheToothLengthwiseDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProjectedLengthOfTheInstantaneousContactLineInTheToothLengthwiseDirection

        if temp is None:
            return None

        return temp

    @property
    def radius_of_curvature_difference_between_point_of_load_and_mean_point(self) -> 'float':
        """float: 'RadiusOfCurvatureDifferenceBetweenPointOfLoadAndMeanPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadiusOfCurvatureDifferenceBetweenPointOfLoadAndMeanPoint

        if temp is None:
            return None

        return temp

    @property
    def relative_fillet_radius_at_root_of_tooth(self) -> 'float':
        """float: 'RelativeFilletRadiusAtRootOfTooth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeFilletRadiusAtRootOfTooth

        if temp is None:
            return None

        return temp

    @property
    def relative_notch_sensitivity_factor(self) -> 'float':
        """float: 'RelativeNotchSensitivityFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeNotchSensitivityFactor

        if temp is None:
            return None

        return temp

    @property
    def relative_surface_condition_factor_for_method_b2(self) -> 'float':
        """float: 'RelativeSurfaceConditionFactorForMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeSurfaceConditionFactorForMethodB2

        if temp is None:
            return None

        return temp

    @property
    def root_stress_adjustment_factor(self) -> 'float':
        """float: 'RootStressAdjustmentFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootStressAdjustmentFactor

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_bending_for_method_b2(self) -> 'float':
        """float: 'SafetyFactorBendingForMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorBendingForMethodB2

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_contact_for_method_b2(self) -> 'float':
        """float: 'SafetyFactorContactForMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorContactForMethodB2

        if temp is None:
            return None

        return temp

    @property
    def stress_concentration_and_correction_factor(self) -> 'float':
        """float: 'StressConcentrationAndCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationAndCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def toe_increment(self) -> 'float':
        """float: 'ToeIncrement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToeIncrement

        if temp is None:
            return None

        return temp

    @property
    def toe_increment_delta_bi(self) -> 'float':
        """float: 'ToeIncrementDeltaBi' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToeIncrementDeltaBi

        if temp is None:
            return None

        return temp

    @property
    def tooth_root_stress_method_b2(self) -> 'float':
        """float: 'ToothRootStressMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootStressMethodB2

        if temp is None:
            return None

        return temp
