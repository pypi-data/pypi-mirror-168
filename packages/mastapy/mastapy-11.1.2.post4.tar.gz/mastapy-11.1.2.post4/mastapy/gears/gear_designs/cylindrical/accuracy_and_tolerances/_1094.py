"""_1094.py

CylindricalAccuracyGrades
"""


from mastapy._internal import constructor
from mastapy.gears import _286
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_ACCURACY_GRADES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'CylindricalAccuracyGrades')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalAccuracyGrades',)


class CylindricalAccuracyGrades(_286.AccuracyGrades):
    """CylindricalAccuracyGrades

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_ACCURACY_GRADES

    def __init__(self, instance_to_wrap: 'CylindricalAccuracyGrades.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def helix_quality_grade(self) -> 'int':
        """int: 'HelixQualityGrade' is the original name of this property."""

        temp = self.wrapped.HelixQualityGrade

        if temp is None:
            return None

        return temp

    @helix_quality_grade.setter
    def helix_quality_grade(self, value: 'int'):
        self.wrapped.HelixQualityGrade = int(value) if value else 0

    @property
    def pitch_quality_grade(self) -> 'int':
        """int: 'PitchQualityGrade' is the original name of this property."""

        temp = self.wrapped.PitchQualityGrade

        if temp is None:
            return None

        return temp

    @pitch_quality_grade.setter
    def pitch_quality_grade(self, value: 'int'):
        self.wrapped.PitchQualityGrade = int(value) if value else 0

    @property
    def profile_quality_grade(self) -> 'int':
        """int: 'ProfileQualityGrade' is the original name of this property."""

        temp = self.wrapped.ProfileQualityGrade

        if temp is None:
            return None

        return temp

    @profile_quality_grade.setter
    def profile_quality_grade(self, value: 'int'):
        self.wrapped.ProfileQualityGrade = int(value) if value else 0

    @property
    def radial_quality_grade(self) -> 'int':
        """int: 'RadialQualityGrade' is the original name of this property."""

        temp = self.wrapped.RadialQualityGrade

        if temp is None:
            return None

        return temp

    @radial_quality_grade.setter
    def radial_quality_grade(self, value: 'int'):
        self.wrapped.RadialQualityGrade = int(value) if value else 0
