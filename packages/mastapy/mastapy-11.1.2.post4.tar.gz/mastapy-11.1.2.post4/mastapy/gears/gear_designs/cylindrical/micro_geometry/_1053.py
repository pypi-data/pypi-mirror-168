"""_1053.py

CylindricalGearBiasModification
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy.gears.micro_geometry import _535
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_BIAS_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearBiasModification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearBiasModification',)


class CylindricalGearBiasModification(_535.BiasModification):
    """CylindricalGearBiasModification

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_BIAS_MODIFICATION

    def __init__(self, instance_to_wrap: 'CylindricalGearBiasModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lead_evaluation_left_limit(self) -> 'float':
        """float: 'LeadEvaluationLeftLimit' is the original name of this property."""

        temp = self.wrapped.LeadEvaluationLeftLimit

        if temp is None:
            return None

        return temp

    @lead_evaluation_left_limit.setter
    def lead_evaluation_left_limit(self, value: 'float'):
        self.wrapped.LeadEvaluationLeftLimit = float(value) if value else 0.0

    @property
    def lead_evaluation_right_limit(self) -> 'float':
        """float: 'LeadEvaluationRightLimit' is the original name of this property."""

        temp = self.wrapped.LeadEvaluationRightLimit

        if temp is None:
            return None

        return temp

    @lead_evaluation_right_limit.setter
    def lead_evaluation_right_limit(self, value: 'float'):
        self.wrapped.LeadEvaluationRightLimit = float(value) if value else 0.0

    @property
    def pressure_angle_mod_at_left_limit(self) -> 'float':
        """float: 'PressureAngleModAtLeftLimit' is the original name of this property."""

        temp = self.wrapped.PressureAngleModAtLeftLimit

        if temp is None:
            return None

        return temp

    @pressure_angle_mod_at_left_limit.setter
    def pressure_angle_mod_at_left_limit(self, value: 'float'):
        self.wrapped.PressureAngleModAtLeftLimit = float(value) if value else 0.0

    @property
    def pressure_angle_mod_at_right_limit(self) -> 'float':
        """float: 'PressureAngleModAtRightLimit' is the original name of this property."""

        temp = self.wrapped.PressureAngleModAtRightLimit

        if temp is None:
            return None

        return temp

    @pressure_angle_mod_at_right_limit.setter
    def pressure_angle_mod_at_right_limit(self, value: 'float'):
        self.wrapped.PressureAngleModAtRightLimit = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_diameter(self) -> 'float':
        """float: 'ProfileEvaluationLowerLimitDiameter' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationLowerLimitDiameter

        if temp is None:
            return None

        return temp

    @profile_evaluation_lower_limit_diameter.setter
    def profile_evaluation_lower_limit_diameter(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitDiameter = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_radius(self) -> 'float':
        """float: 'ProfileEvaluationLowerLimitRadius' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationLowerLimitRadius

        if temp is None:
            return None

        return temp

    @profile_evaluation_lower_limit_radius.setter
    def profile_evaluation_lower_limit_radius(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitRadius = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_roll_angle(self) -> 'float':
        """float: 'ProfileEvaluationLowerLimitRollAngle' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationLowerLimitRollAngle

        if temp is None:
            return None

        return temp

    @profile_evaluation_lower_limit_roll_angle.setter
    def profile_evaluation_lower_limit_roll_angle(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitRollAngle = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_roll_distance(self) -> 'float':
        """float: 'ProfileEvaluationLowerLimitRollDistance' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationLowerLimitRollDistance

        if temp is None:
            return None

        return temp

    @profile_evaluation_lower_limit_roll_distance.setter
    def profile_evaluation_lower_limit_roll_distance(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitRollDistance = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_diameter(self) -> 'float':
        """float: 'ProfileEvaluationUpperLimitDiameter' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationUpperLimitDiameter

        if temp is None:
            return None

        return temp

    @profile_evaluation_upper_limit_diameter.setter
    def profile_evaluation_upper_limit_diameter(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitDiameter = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_radius(self) -> 'float':
        """float: 'ProfileEvaluationUpperLimitRadius' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationUpperLimitRadius

        if temp is None:
            return None

        return temp

    @profile_evaluation_upper_limit_radius.setter
    def profile_evaluation_upper_limit_radius(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitRadius = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_roll_angle(self) -> 'float':
        """float: 'ProfileEvaluationUpperLimitRollAngle' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationUpperLimitRollAngle

        if temp is None:
            return None

        return temp

    @profile_evaluation_upper_limit_roll_angle.setter
    def profile_evaluation_upper_limit_roll_angle(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitRollAngle = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_roll_distance(self) -> 'float':
        """float: 'ProfileEvaluationUpperLimitRollDistance' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationUpperLimitRollDistance

        if temp is None:
            return None

        return temp

    @profile_evaluation_upper_limit_roll_distance.setter
    def profile_evaluation_upper_limit_roll_distance(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitRollDistance = float(value) if value else 0.0

    @property
    def relief_at_left_limit_isoagmadin(self) -> 'float':
        """float: 'ReliefAtLeftLimitISOAGMADIN' is the original name of this property."""

        temp = self.wrapped.ReliefAtLeftLimitISOAGMADIN

        if temp is None:
            return None

        return temp

    @relief_at_left_limit_isoagmadin.setter
    def relief_at_left_limit_isoagmadin(self, value: 'float'):
        self.wrapped.ReliefAtLeftLimitISOAGMADIN = float(value) if value else 0.0

    @property
    def relief_at_left_limit_ldp(self) -> 'float':
        """float: 'ReliefAtLeftLimitLDP' is the original name of this property."""

        temp = self.wrapped.ReliefAtLeftLimitLDP

        if temp is None:
            return None

        return temp

    @relief_at_left_limit_ldp.setter
    def relief_at_left_limit_ldp(self, value: 'float'):
        self.wrapped.ReliefAtLeftLimitLDP = float(value) if value else 0.0

    @property
    def relief_at_left_limit_vdi(self) -> 'float':
        """float: 'ReliefAtLeftLimitVDI' is the original name of this property."""

        temp = self.wrapped.ReliefAtLeftLimitVDI

        if temp is None:
            return None

        return temp

    @relief_at_left_limit_vdi.setter
    def relief_at_left_limit_vdi(self, value: 'float'):
        self.wrapped.ReliefAtLeftLimitVDI = float(value) if value else 0.0

    @property
    def relief_at_right_limit_isoagmadin(self) -> 'float':
        """float: 'ReliefAtRightLimitISOAGMADIN' is the original name of this property."""

        temp = self.wrapped.ReliefAtRightLimitISOAGMADIN

        if temp is None:
            return None

        return temp

    @relief_at_right_limit_isoagmadin.setter
    def relief_at_right_limit_isoagmadin(self, value: 'float'):
        self.wrapped.ReliefAtRightLimitISOAGMADIN = float(value) if value else 0.0

    @property
    def relief_at_right_limit_ldp(self) -> 'float':
        """float: 'ReliefAtRightLimitLDP' is the original name of this property."""

        temp = self.wrapped.ReliefAtRightLimitLDP

        if temp is None:
            return None

        return temp

    @relief_at_right_limit_ldp.setter
    def relief_at_right_limit_ldp(self, value: 'float'):
        self.wrapped.ReliefAtRightLimitLDP = float(value) if value else 0.0

    @property
    def relief_at_right_limit_vdi(self) -> 'float':
        """float: 'ReliefAtRightLimitVDI' is the original name of this property."""

        temp = self.wrapped.ReliefAtRightLimitVDI

        if temp is None:
            return None

        return temp

    @relief_at_right_limit_vdi.setter
    def relief_at_right_limit_vdi(self, value: 'float'):
        self.wrapped.ReliefAtRightLimitVDI = float(value) if value else 0.0

    @property
    def zero_bias_relief(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ZeroBiasRelief' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZeroBiasRelief

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_evaluation_lower_limit(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileEvaluationLowerLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileEvaluationLowerLimit

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_evaluation_upper_limit(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileEvaluationUpperLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileEvaluationUpperLimit

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def relief_of(self, face_width: 'float', roll_distance: 'float') -> 'float':
        """ 'ReliefOf' is the original name of this method.

        Args:
            face_width (float)
            roll_distance (float)

        Returns:
            float
        """

        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = self.wrapped.ReliefOf(face_width if face_width else 0.0, roll_distance if roll_distance else 0.0)
        return method_result
