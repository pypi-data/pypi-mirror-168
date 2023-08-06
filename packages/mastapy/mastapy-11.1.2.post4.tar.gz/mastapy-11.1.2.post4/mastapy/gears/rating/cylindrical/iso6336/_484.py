"""_484.py

ISO6336AbstractGearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical import _435
from mastapy._internal.python_net import python_net_import

_ISO6336_ABSTRACT_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336AbstractGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336AbstractGearSingleFlankRating',)


class ISO6336AbstractGearSingleFlankRating(_435.CylindricalGearSingleFlankRating):
    """ISO6336AbstractGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _ISO6336_ABSTRACT_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'ISO6336AbstractGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def e(self) -> 'float':
        """float: 'E' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.E

        if temp is None:
            return None

        return temp

    @property
    def face_width_for_root_stress(self) -> 'float':
        """float: 'FaceWidthForRootStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidthForRootStress

        if temp is None:
            return None

        return temp

    @property
    def form_factor(self) -> 'float':
        """float: 'FormFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormFactor

        if temp is None:
            return None

        return temp

    @property
    def g(self) -> 'float':
        """float: 'G' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.G

        if temp is None:
            return None

        return temp

    @property
    def h(self) -> 'float':
        """float: 'H' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.H

        if temp is None:
            return None

        return temp

    @property
    def intermediate_angle(self) -> 'float':
        """float: 'IntermediateAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IntermediateAngle

        if temp is None:
            return None

        return temp

    @property
    def nominal_tooth_root_stress(self) -> 'float':
        """float: 'NominalToothRootStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalToothRootStress

        if temp is None:
            return None

        return temp

    @property
    def notch_parameter(self) -> 'float':
        """float: 'NotchParameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NotchParameter

        if temp is None:
            return None

        return temp

    @property
    def roughness_factor(self) -> 'float':
        """float: 'RoughnessFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoughnessFactor

        if temp is None:
            return None

        return temp

    @property
    def stress_correction_factor(self) -> 'float':
        """float: 'StressCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def stress_correction_factor_bending_for_test_gears(self) -> 'float':
        """float: 'StressCorrectionFactorBendingForTestGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCorrectionFactorBendingForTestGears

        if temp is None:
            return None

        return temp
