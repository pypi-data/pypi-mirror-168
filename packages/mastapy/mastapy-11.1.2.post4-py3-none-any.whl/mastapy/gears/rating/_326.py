"""_326.py

AbstractGearRating
"""


from mastapy._internal import constructor
from mastapy.gears.analysis import _1167
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'AbstractGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractGearRating',)


class AbstractGearRating(_1167.AbstractGearAnalysis):
    """AbstractGearRating

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_GEAR_RATING

    def __init__(self, instance_to_wrap: 'AbstractGearRating.TYPE'):
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
    def bending_safety_factor_for_static(self) -> 'float':
        """float: 'BendingSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingSafetyFactorForStatic

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
    def contact_safety_factor_for_static(self) -> 'float':
        """float: 'ContactSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactSafetyFactorForStatic

        if temp is None:
            return None

        return temp

    @property
    def cycles_to_fail(self) -> 'float':
        """float: 'CyclesToFail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CyclesToFail

        if temp is None:
            return None

        return temp

    @property
    def cycles_to_fail_bending(self) -> 'float':
        """float: 'CyclesToFailBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CyclesToFailBending

        if temp is None:
            return None

        return temp

    @property
    def cycles_to_fail_contact(self) -> 'float':
        """float: 'CyclesToFailContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CyclesToFailContact

        if temp is None:
            return None

        return temp

    @property
    def damage_bending(self) -> 'float':
        """float: 'DamageBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DamageBending

        if temp is None:
            return None

        return temp

    @property
    def damage_contact(self) -> 'float':
        """float: 'DamageContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DamageContact

        if temp is None:
            return None

        return temp

    @property
    def gear_reliability_bending(self) -> 'float':
        """float: 'GearReliabilityBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearReliabilityBending

        if temp is None:
            return None

        return temp

    @property
    def gear_reliability_contact(self) -> 'float':
        """float: 'GearReliabilityContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearReliabilityContact

        if temp is None:
            return None

        return temp

    @property
    def normalized_bending_safety_factor_for_fatigue(self) -> 'float':
        """float: 'NormalizedBendingSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalizedBendingSafetyFactorForFatigue

        if temp is None:
            return None

        return temp

    @property
    def normalized_bending_safety_factor_for_static(self) -> 'float':
        """float: 'NormalizedBendingSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalizedBendingSafetyFactorForStatic

        if temp is None:
            return None

        return temp

    @property
    def normalized_contact_safety_factor_for_fatigue(self) -> 'float':
        """float: 'NormalizedContactSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalizedContactSafetyFactorForFatigue

        if temp is None:
            return None

        return temp

    @property
    def normalized_contact_safety_factor_for_static(self) -> 'float':
        """float: 'NormalizedContactSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalizedContactSafetyFactorForStatic

        if temp is None:
            return None

        return temp

    @property
    def normalized_safety_factor_for_fatigue(self) -> 'float':
        """float: 'NormalizedSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalizedSafetyFactorForFatigue

        if temp is None:
            return None

        return temp

    @property
    def normalized_safety_factor_for_static(self) -> 'float':
        """float: 'NormalizedSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalizedSafetyFactorForStatic

        if temp is None:
            return None

        return temp

    @property
    def time_to_fail(self) -> 'float':
        """float: 'TimeToFail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeToFail

        if temp is None:
            return None

        return temp

    @property
    def time_to_fail_bending(self) -> 'float':
        """float: 'TimeToFailBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeToFailBending

        if temp is None:
            return None

        return temp

    @property
    def time_to_fail_contact(self) -> 'float':
        """float: 'TimeToFailContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeToFailContact

        if temp is None:
            return None

        return temp

    @property
    def total_gear_reliability(self) -> 'float':
        """float: 'TotalGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalGearReliability

        if temp is None:
            return None

        return temp
