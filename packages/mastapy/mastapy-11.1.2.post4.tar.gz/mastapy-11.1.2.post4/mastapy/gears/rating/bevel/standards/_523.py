"""_523.py

AGMASpiralBevelGearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.bevel.standards import _527
from mastapy._internal.python_net import python_net_import

_AGMA_SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel.Standards', 'AGMASpiralBevelGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMASpiralBevelGearSingleFlankRating',)


class AGMASpiralBevelGearSingleFlankRating(_527.SpiralBevelGearSingleFlankRating):
    """AGMASpiralBevelGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _AGMA_SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'AGMASpiralBevelGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_safety_factor_for_fatigue(self) -> 'float':
        """float: 'BendingSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingSafetyFactorForFatigue

        if temp is None:
            return None

        return temp

    @property
    def calculated_bending_stress(self) -> 'float':
        """float: 'CalculatedBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedBendingStress

        if temp is None:
            return None

        return temp

    @property
    def calculated_contact_stress(self) -> 'float':
        """float: 'CalculatedContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedContactStress

        if temp is None:
            return None

        return temp

    @property
    def contact_safety_factor_for_fatigue(self) -> 'float':
        """float: 'ContactSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactSafetyFactorForFatigue

        if temp is None:
            return None

        return temp

    @property
    def hardness_ratio_factor(self) -> 'float':
        """float: 'HardnessRatioFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HardnessRatioFactor

        if temp is None:
            return None

        return temp

    @property
    def permissible_bending_stress(self) -> 'float':
        """float: 'PermissibleBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleBendingStress

        if temp is None:
            return None

        return temp

    @property
    def permissible_contact_stress(self) -> 'float':
        """float: 'PermissibleContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleContactStress

        if temp is None:
            return None

        return temp

    @property
    def stress_cycle_factor_bending(self) -> 'float':
        """float: 'StressCycleFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCycleFactorBending

        if temp is None:
            return None

        return temp

    @property
    def stress_cycle_factor_contact(self) -> 'float':
        """float: 'StressCycleFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCycleFactorContact

        if temp is None:
            return None

        return temp
