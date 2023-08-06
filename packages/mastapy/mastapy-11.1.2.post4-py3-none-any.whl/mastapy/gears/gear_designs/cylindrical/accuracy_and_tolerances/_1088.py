"""_1088.py

AGMA2000AccuracyGrader
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1092
from mastapy._internal.python_net import python_net_import

_AGMA2000_ACCURACY_GRADER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'AGMA2000AccuracyGrader')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMA2000AccuracyGrader',)


class AGMA2000AccuracyGrader(_1092.CylindricalAccuracyGrader):
    """AGMA2000AccuracyGrader

    This is a mastapy class.
    """

    TYPE = _AGMA2000_ACCURACY_GRADER

    def __init__(self, instance_to_wrap: 'AGMA2000AccuracyGrader.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def adjusted_number_of_teeth(self) -> 'float':
        """float: 'AdjustedNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdjustedNumberOfTeeth

        if temp is None:
            return None

        return temp

    @property
    def composite_tolerance_toothto_tooth(self) -> 'float':
        """float: 'CompositeToleranceToothtoTooth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompositeToleranceToothtoTooth

        if temp is None:
            return None

        return temp

    @property
    def pitch_variation_allowable(self) -> 'float':
        """float: 'PitchVariationAllowable' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchVariationAllowable

        if temp is None:
            return None

        return temp

    @property
    def profile_tolerance(self) -> 'float':
        """float: 'ProfileTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileTolerance

        if temp is None:
            return None

        return temp

    @property
    def runout_radial_tolerance(self) -> 'float':
        """float: 'RunoutRadialTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunoutRadialTolerance

        if temp is None:
            return None

        return temp

    @property
    def tooth_alignment_tolerance(self) -> 'float':
        """float: 'ToothAlignmentTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothAlignmentTolerance

        if temp is None:
            return None

        return temp

    @property
    def total_composite_tolerance(self) -> 'float':
        """float: 'TotalCompositeTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalCompositeTolerance

        if temp is None:
            return None

        return temp
