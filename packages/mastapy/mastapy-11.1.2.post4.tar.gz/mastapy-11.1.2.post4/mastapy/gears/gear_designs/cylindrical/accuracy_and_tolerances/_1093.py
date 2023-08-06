"""_1093.py

CylindricalAccuracyGraderWithProfileFormAndSlope
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1092
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_ACCURACY_GRADER_WITH_PROFILE_FORM_AND_SLOPE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'CylindricalAccuracyGraderWithProfileFormAndSlope')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalAccuracyGraderWithProfileFormAndSlope',)


class CylindricalAccuracyGraderWithProfileFormAndSlope(_1092.CylindricalAccuracyGrader):
    """CylindricalAccuracyGraderWithProfileFormAndSlope

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_ACCURACY_GRADER_WITH_PROFILE_FORM_AND_SLOPE

    def __init__(self, instance_to_wrap: 'CylindricalAccuracyGraderWithProfileFormAndSlope.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cumulative_pitch_deviation(self) -> 'float':
        """float: 'CumulativePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CumulativePitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def helix_form_deviation(self) -> 'float':
        """float: 'HelixFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixFormDeviation

        if temp is None:
            return None

        return temp

    @property
    def helix_slope_deviation(self) -> 'float':
        """float: 'HelixSlopeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixSlopeDeviation

        if temp is None:
            return None

        return temp

    @property
    def helix_slope_deviation_per_inch_face_width(self) -> 'float':
        """float: 'HelixSlopeDeviationPerInchFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixSlopeDeviationPerInchFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def number_of_pitches_for_sector_pitch_deviation(self) -> 'int':
        """int: 'NumberOfPitchesForSectorPitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfPitchesForSectorPitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def profile_form_deviation(self) -> 'float':
        """float: 'ProfileFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileFormDeviation

        if temp is None:
            return None

        return temp

    @property
    def profile_slope_deviation(self) -> 'float':
        """float: 'ProfileSlopeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileSlopeDeviation

        if temp is None:
            return None

        return temp

    @property
    def total_cumulative_pitch_deviation(self) -> 'float':
        """float: 'TotalCumulativePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalCumulativePitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def total_helix_deviation(self) -> 'float':
        """float: 'TotalHelixDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalHelixDeviation

        if temp is None:
            return None

        return temp

    @property
    def total_profile_deviation(self) -> 'float':
        """float: 'TotalProfileDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalProfileDeviation

        if temp is None:
            return None

        return temp
