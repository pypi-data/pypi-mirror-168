"""_607.py

ShapingProcessSimulation
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.process_simulation import _605
from mastapy._internal.python_net import python_net_import

_SHAPING_PROCESS_SIMULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.ProcessSimulation', 'ShapingProcessSimulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ShapingProcessSimulation',)


class ShapingProcessSimulation(_605.CutterProcessSimulation):
    """ShapingProcessSimulation

    This is a mastapy class.
    """

    TYPE = _SHAPING_PROCESS_SIMULATION

    def __init__(self, instance_to_wrap: 'ShapingProcessSimulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def circle_blade_flank_angle_error(self) -> 'float':
        """float: 'CircleBladeFlankAngleError' is the original name of this property."""

        temp = self.wrapped.CircleBladeFlankAngleError

        if temp is None:
            return None

        return temp

    @circle_blade_flank_angle_error.setter
    def circle_blade_flank_angle_error(self, value: 'float'):
        self.wrapped.CircleBladeFlankAngleError = float(value) if value else 0.0

    @property
    def circle_blade_rake_angle_error(self) -> 'float':
        """float: 'CircleBladeRakeAngleError' is the original name of this property."""

        temp = self.wrapped.CircleBladeRakeAngleError

        if temp is None:
            return None

        return temp

    @circle_blade_rake_angle_error.setter
    def circle_blade_rake_angle_error(self, value: 'float'):
        self.wrapped.CircleBladeRakeAngleError = float(value) if value else 0.0

    @property
    def circumstance_feed(self) -> 'float':
        """float: 'CircumstanceFeed' is the original name of this property."""

        temp = self.wrapped.CircumstanceFeed

        if temp is None:
            return None

        return temp

    @circumstance_feed.setter
    def circumstance_feed(self, value: 'float'):
        self.wrapped.CircumstanceFeed = float(value) if value else 0.0

    @property
    def deviation_in_x_direction(self) -> 'float':
        """float: 'DeviationInXDirection' is the original name of this property."""

        temp = self.wrapped.DeviationInXDirection

        if temp is None:
            return None

        return temp

    @deviation_in_x_direction.setter
    def deviation_in_x_direction(self, value: 'float'):
        self.wrapped.DeviationInXDirection = float(value) if value else 0.0

    @property
    def deviation_in_y_direction(self) -> 'float':
        """float: 'DeviationInYDirection' is the original name of this property."""

        temp = self.wrapped.DeviationInYDirection

        if temp is None:
            return None

        return temp

    @deviation_in_y_direction.setter
    def deviation_in_y_direction(self, value: 'float'):
        self.wrapped.DeviationInYDirection = float(value) if value else 0.0

    @property
    def distance_between_two_sections(self) -> 'float':
        """float: 'DistanceBetweenTwoSections' is the original name of this property."""

        temp = self.wrapped.DistanceBetweenTwoSections

        if temp is None:
            return None

        return temp

    @distance_between_two_sections.setter
    def distance_between_two_sections(self, value: 'float'):
        self.wrapped.DistanceBetweenTwoSections = float(value) if value else 0.0

    @property
    def eap_diameter(self) -> 'float':
        """float: 'EAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EAPDiameter

        if temp is None:
            return None

        return temp

    @property
    def face_runout(self) -> 'float':
        """float: 'FaceRunout' is the original name of this property."""

        temp = self.wrapped.FaceRunout

        if temp is None:
            return None

        return temp

    @face_runout.setter
    def face_runout(self, value: 'float'):
        self.wrapped.FaceRunout = float(value) if value else 0.0

    @property
    def face_runout_check_diameter(self) -> 'float':
        """float: 'FaceRunoutCheckDiameter' is the original name of this property."""

        temp = self.wrapped.FaceRunoutCheckDiameter

        if temp is None:
            return None

        return temp

    @face_runout_check_diameter.setter
    def face_runout_check_diameter(self, value: 'float'):
        self.wrapped.FaceRunoutCheckDiameter = float(value) if value else 0.0

    @property
    def factor(self) -> 'float':
        """float: 'Factor' is the original name of this property."""

        temp = self.wrapped.Factor

        if temp is None:
            return None

        return temp

    @factor.setter
    def factor(self, value: 'float'):
        self.wrapped.Factor = float(value) if value else 0.0

    @property
    def first_phase_maximum_angle(self) -> 'float':
        """float: 'FirstPhaseMaximumAngle' is the original name of this property."""

        temp = self.wrapped.FirstPhaseMaximumAngle

        if temp is None:
            return None

        return temp

    @first_phase_maximum_angle.setter
    def first_phase_maximum_angle(self, value: 'float'):
        self.wrapped.FirstPhaseMaximumAngle = float(value) if value else 0.0

    @property
    def first_section_runout(self) -> 'float':
        """float: 'FirstSectionRunout' is the original name of this property."""

        temp = self.wrapped.FirstSectionRunout

        if temp is None:
            return None

        return temp

    @first_section_runout.setter
    def first_section_runout(self, value: 'float'):
        self.wrapped.FirstSectionRunout = float(value) if value else 0.0

    @property
    def pressure_angle_error_left_flank(self) -> 'float':
        """float: 'PressureAngleErrorLeftFlank' is the original name of this property."""

        temp = self.wrapped.PressureAngleErrorLeftFlank

        if temp is None:
            return None

        return temp

    @pressure_angle_error_left_flank.setter
    def pressure_angle_error_left_flank(self, value: 'float'):
        self.wrapped.PressureAngleErrorLeftFlank = float(value) if value else 0.0

    @property
    def pressure_angle_error_right_flank(self) -> 'float':
        """float: 'PressureAngleErrorRightFlank' is the original name of this property."""

        temp = self.wrapped.PressureAngleErrorRightFlank

        if temp is None:
            return None

        return temp

    @pressure_angle_error_right_flank.setter
    def pressure_angle_error_right_flank(self, value: 'float'):
        self.wrapped.PressureAngleErrorRightFlank = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit(self) -> 'float':
        """float: 'ProfileEvaluationLowerLimit' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationLowerLimit

        if temp is None:
            return None

        return temp

    @profile_evaluation_lower_limit.setter
    def profile_evaluation_lower_limit(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimit = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit(self) -> 'float':
        """float: 'ProfileEvaluationUpperLimit' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationUpperLimit

        if temp is None:
            return None

        return temp

    @profile_evaluation_upper_limit.setter
    def profile_evaluation_upper_limit(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimit = float(value) if value else 0.0

    @property
    def second_phase_max_angle(self) -> 'float':
        """float: 'SecondPhaseMaxAngle' is the original name of this property."""

        temp = self.wrapped.SecondPhaseMaxAngle

        if temp is None:
            return None

        return temp

    @second_phase_max_angle.setter
    def second_phase_max_angle(self, value: 'float'):
        self.wrapped.SecondPhaseMaxAngle = float(value) if value else 0.0

    @property
    def second_section_runout(self) -> 'float':
        """float: 'SecondSectionRunout' is the original name of this property."""

        temp = self.wrapped.SecondSectionRunout

        if temp is None:
            return None

        return temp

    @second_section_runout.setter
    def second_section_runout(self, value: 'float'):
        self.wrapped.SecondSectionRunout = float(value) if value else 0.0

    @property
    def shaper_cumulative_pitch_error_left_flank(self) -> 'float':
        """float: 'ShaperCumulativePitchErrorLeftFlank' is the original name of this property."""

        temp = self.wrapped.ShaperCumulativePitchErrorLeftFlank

        if temp is None:
            return None

        return temp

    @shaper_cumulative_pitch_error_left_flank.setter
    def shaper_cumulative_pitch_error_left_flank(self, value: 'float'):
        self.wrapped.ShaperCumulativePitchErrorLeftFlank = float(value) if value else 0.0

    @property
    def shaper_cumulative_pitch_error_right_flank(self) -> 'float':
        """float: 'ShaperCumulativePitchErrorRightFlank' is the original name of this property."""

        temp = self.wrapped.ShaperCumulativePitchErrorRightFlank

        if temp is None:
            return None

        return temp

    @shaper_cumulative_pitch_error_right_flank.setter
    def shaper_cumulative_pitch_error_right_flank(self, value: 'float'):
        self.wrapped.ShaperCumulativePitchErrorRightFlank = float(value) if value else 0.0

    @property
    def shaper_radial_runout(self) -> 'float':
        """float: 'ShaperRadialRunout' is the original name of this property."""

        temp = self.wrapped.ShaperRadialRunout

        if temp is None:
            return None

        return temp

    @shaper_radial_runout.setter
    def shaper_radial_runout(self, value: 'float'):
        self.wrapped.ShaperRadialRunout = float(value) if value else 0.0

    @property
    def shaper_stoke(self) -> 'float':
        """float: 'ShaperStoke' is the original name of this property."""

        temp = self.wrapped.ShaperStoke

        if temp is None:
            return None

        return temp

    @shaper_stoke.setter
    def shaper_stoke(self, value: 'float'):
        self.wrapped.ShaperStoke = float(value) if value else 0.0

    @property
    def shaper_tilt_angle(self) -> 'float':
        """float: 'ShaperTiltAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaperTiltAngle

        if temp is None:
            return None

        return temp

    @property
    def spindle_angle_at_maximum_face_runout(self) -> 'float':
        """float: 'SpindleAngleAtMaximumFaceRunout' is the original name of this property."""

        temp = self.wrapped.SpindleAngleAtMaximumFaceRunout

        if temp is None:
            return None

        return temp

    @spindle_angle_at_maximum_face_runout.setter
    def spindle_angle_at_maximum_face_runout(self, value: 'float'):
        self.wrapped.SpindleAngleAtMaximumFaceRunout = float(value) if value else 0.0

    @property
    def spindle_angle_at_maximum_radial_runout(self) -> 'float':
        """float: 'SpindleAngleAtMaximumRadialRunout' is the original name of this property."""

        temp = self.wrapped.SpindleAngleAtMaximumRadialRunout

        if temp is None:
            return None

        return temp

    @spindle_angle_at_maximum_radial_runout.setter
    def spindle_angle_at_maximum_radial_runout(self, value: 'float'):
        self.wrapped.SpindleAngleAtMaximumRadialRunout = float(value) if value else 0.0

    @property
    def test_distance_in_x_direction(self) -> 'float':
        """float: 'TestDistanceInXDirection' is the original name of this property."""

        temp = self.wrapped.TestDistanceInXDirection

        if temp is None:
            return None

        return temp

    @test_distance_in_x_direction.setter
    def test_distance_in_x_direction(self, value: 'float'):
        self.wrapped.TestDistanceInXDirection = float(value) if value else 0.0

    @property
    def test_distance_in_y_direction(self) -> 'float':
        """float: 'TestDistanceInYDirection' is the original name of this property."""

        temp = self.wrapped.TestDistanceInYDirection

        if temp is None:
            return None

        return temp

    @test_distance_in_y_direction.setter
    def test_distance_in_y_direction(self, value: 'float'):
        self.wrapped.TestDistanceInYDirection = float(value) if value else 0.0

    @property
    def use_sin_curve_for_shaper_pitch_error(self) -> 'bool':
        """bool: 'UseSinCurveForShaperPitchError' is the original name of this property."""

        temp = self.wrapped.UseSinCurveForShaperPitchError

        if temp is None:
            return None

        return temp

    @use_sin_curve_for_shaper_pitch_error.setter
    def use_sin_curve_for_shaper_pitch_error(self, value: 'bool'):
        self.wrapped.UseSinCurveForShaperPitchError = bool(value) if value else False
