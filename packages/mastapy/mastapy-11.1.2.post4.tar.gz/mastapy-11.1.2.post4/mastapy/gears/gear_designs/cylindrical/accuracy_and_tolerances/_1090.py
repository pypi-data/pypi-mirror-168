"""_1090.py

AGMA20151AccuracyGrades
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1094
from mastapy._internal.python_net import python_net_import

_AGMA20151_ACCURACY_GRADES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'AGMA20151AccuracyGrades')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMA20151AccuracyGrades',)


class AGMA20151AccuracyGrades(_1094.CylindricalAccuracyGrades):
    """AGMA20151AccuracyGrades

    This is a mastapy class.
    """

    TYPE = _AGMA20151_ACCURACY_GRADES

    def __init__(self, instance_to_wrap: 'AGMA20151AccuracyGrades.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def helix_agma_quality_grade_new(self) -> 'int':
        """int: 'HelixAGMAQualityGradeNew' is the original name of this property."""

        temp = self.wrapped.HelixAGMAQualityGradeNew

        if temp is None:
            return None

        return temp

    @helix_agma_quality_grade_new.setter
    def helix_agma_quality_grade_new(self, value: 'int'):
        self.wrapped.HelixAGMAQualityGradeNew = int(value) if value else 0

    @property
    def helix_agma_quality_grade_old(self) -> 'int':
        """int: 'HelixAGMAQualityGradeOld' is the original name of this property."""

        temp = self.wrapped.HelixAGMAQualityGradeOld

        if temp is None:
            return None

        return temp

    @helix_agma_quality_grade_old.setter
    def helix_agma_quality_grade_old(self, value: 'int'):
        self.wrapped.HelixAGMAQualityGradeOld = int(value) if value else 0

    @property
    def input_single_pitch_deviation(self) -> 'bool':
        """bool: 'InputSinglePitchDeviation' is the original name of this property."""

        temp = self.wrapped.InputSinglePitchDeviation

        if temp is None:
            return None

        return temp

    @input_single_pitch_deviation.setter
    def input_single_pitch_deviation(self, value: 'bool'):
        self.wrapped.InputSinglePitchDeviation = bool(value) if value else False

    @property
    def pitch_agma_quality_grade_new(self) -> 'int':
        """int: 'PitchAGMAQualityGradeNew' is the original name of this property."""

        temp = self.wrapped.PitchAGMAQualityGradeNew

        if temp is None:
            return None

        return temp

    @pitch_agma_quality_grade_new.setter
    def pitch_agma_quality_grade_new(self, value: 'int'):
        self.wrapped.PitchAGMAQualityGradeNew = int(value) if value else 0

    @property
    def pitch_agma_quality_grade_old(self) -> 'int':
        """int: 'PitchAGMAQualityGradeOld' is the original name of this property."""

        temp = self.wrapped.PitchAGMAQualityGradeOld

        if temp is None:
            return None

        return temp

    @pitch_agma_quality_grade_old.setter
    def pitch_agma_quality_grade_old(self, value: 'int'):
        self.wrapped.PitchAGMAQualityGradeOld = int(value) if value else 0

    @property
    def profile_agma_quality_grade_new(self) -> 'int':
        """int: 'ProfileAGMAQualityGradeNew' is the original name of this property."""

        temp = self.wrapped.ProfileAGMAQualityGradeNew

        if temp is None:
            return None

        return temp

    @profile_agma_quality_grade_new.setter
    def profile_agma_quality_grade_new(self, value: 'int'):
        self.wrapped.ProfileAGMAQualityGradeNew = int(value) if value else 0

    @property
    def profile_agma_quality_grade_old(self) -> 'int':
        """int: 'ProfileAGMAQualityGradeOld' is the original name of this property."""

        temp = self.wrapped.ProfileAGMAQualityGradeOld

        if temp is None:
            return None

        return temp

    @profile_agma_quality_grade_old.setter
    def profile_agma_quality_grade_old(self, value: 'int'):
        self.wrapped.ProfileAGMAQualityGradeOld = int(value) if value else 0

    @property
    def radial_agma_quality_grade_new(self) -> 'int':
        """int: 'RadialAGMAQualityGradeNew' is the original name of this property."""

        temp = self.wrapped.RadialAGMAQualityGradeNew

        if temp is None:
            return None

        return temp

    @radial_agma_quality_grade_new.setter
    def radial_agma_quality_grade_new(self, value: 'int'):
        self.wrapped.RadialAGMAQualityGradeNew = int(value) if value else 0

    @property
    def radial_agma_quality_grade_old(self) -> 'int':
        """int: 'RadialAGMAQualityGradeOld' is the original name of this property."""

        temp = self.wrapped.RadialAGMAQualityGradeOld

        if temp is None:
            return None

        return temp

    @radial_agma_quality_grade_old.setter
    def radial_agma_quality_grade_old(self, value: 'int'):
        self.wrapped.RadialAGMAQualityGradeOld = int(value) if value else 0

    @property
    def single_pitch_deviation_agma(self) -> 'float':
        """float: 'SinglePitchDeviationAGMA' is the original name of this property."""

        temp = self.wrapped.SinglePitchDeviationAGMA

        if temp is None:
            return None

        return temp

    @single_pitch_deviation_agma.setter
    def single_pitch_deviation_agma(self, value: 'float'):
        self.wrapped.SinglePitchDeviationAGMA = float(value) if value else 0.0
