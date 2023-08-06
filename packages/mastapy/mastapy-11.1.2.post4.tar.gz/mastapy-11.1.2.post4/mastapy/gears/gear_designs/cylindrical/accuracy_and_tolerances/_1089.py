"""_1089.py

AGMA20151AccuracyGrader
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1093
from mastapy._internal.python_net import python_net_import

_AGMA20151_ACCURACY_GRADER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'AGMA20151AccuracyGrader')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMA20151AccuracyGrader',)


class AGMA20151AccuracyGrader(_1093.CylindricalAccuracyGraderWithProfileFormAndSlope):
    """AGMA20151AccuracyGrader

    This is a mastapy class.
    """

    TYPE = _AGMA20151_ACCURACY_GRADER

    def __init__(self, instance_to_wrap: 'AGMA20151AccuracyGrader.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cumulative_pitch_tolerance(self) -> 'float':
        """float: 'CumulativePitchTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CumulativePitchTolerance

        if temp is None:
            return None

        return temp

    @property
    def helix_form_tolerance(self) -> 'float':
        """float: 'HelixFormTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixFormTolerance

        if temp is None:
            return None

        return temp

    @property
    def helix_slope_tolerance(self) -> 'float':
        """float: 'HelixSlopeTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixSlopeTolerance

        if temp is None:
            return None

        return temp

    @property
    def profile_form_tolerance(self) -> 'float':
        """float: 'ProfileFormTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileFormTolerance

        if temp is None:
            return None

        return temp

    @property
    def profile_slope_tolerance(self) -> 'float':
        """float: 'ProfileSlopeTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileSlopeTolerance

        if temp is None:
            return None

        return temp

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
    def sector_pitch_deviation_tolerance(self) -> 'float':
        """float: 'SectorPitchDeviationTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectorPitchDeviationTolerance

        if temp is None:
            return None

        return temp

    @property
    def single_flank_tooth_to_tooth_composite_tolerance(self) -> 'float':
        """float: 'SingleFlankToothToToothCompositeTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleFlankToothToToothCompositeTolerance

        if temp is None:
            return None

        return temp

    @property
    def single_flank_total_composite_tolerance(self) -> 'float':
        """float: 'SingleFlankTotalCompositeTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SingleFlankTotalCompositeTolerance

        if temp is None:
            return None

        return temp

    @property
    def single_pitch_tolerance(self) -> 'float':
        """float: 'SinglePitchTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SinglePitchTolerance

        if temp is None:
            return None

        return temp

    @property
    def specified_single_pitch_deviation(self) -> 'float':
        """float: 'SpecifiedSinglePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedSinglePitchDeviation

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
    def total_helix_tolerance(self) -> 'float':
        """float: 'TotalHelixTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalHelixTolerance

        if temp is None:
            return None

        return temp

    @property
    def total_profile_tolerance(self) -> 'float':
        """float: 'TotalProfileTolerance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalProfileTolerance

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
