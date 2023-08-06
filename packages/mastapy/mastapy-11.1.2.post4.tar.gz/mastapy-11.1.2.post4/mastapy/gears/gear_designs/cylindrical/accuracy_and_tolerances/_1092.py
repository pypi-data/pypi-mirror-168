"""_1092.py

CylindricalAccuracyGrader
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1094, _1090, _1099
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_ACCURACY_GRADER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'CylindricalAccuracyGrader')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalAccuracyGrader',)


class CylindricalAccuracyGrader(_0.APIBase):
    """CylindricalAccuracyGrader

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_ACCURACY_GRADER

    def __init__(self, instance_to_wrap: 'CylindricalAccuracyGrader.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def runout(self) -> 'float':
        """float: 'Runout' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Runout

        if temp is None:
            return None

        return temp

    @property
    def single_pitch_deviation(self) -> 'float':
        """float: 'SinglePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SinglePitchDeviation

        if temp is None:
            return None

        return temp

    @property
    def tolerance_standard(self) -> 'str':
        """str: 'ToleranceStandard' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToleranceStandard

        if temp is None:
            return None

        return temp

    @property
    def toothto_tooth_radial_composite_deviation(self) -> 'float':
        """float: 'ToothtoToothRadialCompositeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothtoToothRadialCompositeDeviation

        if temp is None:
            return None

        return temp

    @property
    def total_radial_composite_deviation(self) -> 'float':
        """float: 'TotalRadialCompositeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalRadialCompositeDeviation

        if temp is None:
            return None

        return temp

    @property
    def accuracy_grades(self) -> '_1094.CylindricalAccuracyGrades':
        """CylindricalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGrades

        if temp is None:
            return None

        if _1094.CylindricalAccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to CylindricalAccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_of_type_agma20151_accuracy_grades(self) -> '_1090.AGMA20151AccuracyGrades':
        """AGMA20151AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGrades

        if temp is None:
            return None

        if _1090.AGMA20151AccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMA20151AccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def accuracy_grades_of_type_iso1328_accuracy_grades(self) -> '_1099.ISO1328AccuracyGrades':
        """ISO1328AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccuracyGrades

        if temp is None:
            return None

        if _1099.ISO1328AccuracyGrades.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to ISO1328AccuracyGrades. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
