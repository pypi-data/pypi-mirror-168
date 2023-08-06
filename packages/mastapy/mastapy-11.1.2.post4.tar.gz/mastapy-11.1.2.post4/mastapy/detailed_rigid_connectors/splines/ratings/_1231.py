"""_1231.py

AGMA6123SplineHalfRating
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.splines.ratings import _1239
from mastapy._internal.python_net import python_net_import

_AGMA6123_SPLINE_HALF_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings', 'AGMA6123SplineHalfRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMA6123SplineHalfRating',)


class AGMA6123SplineHalfRating(_1239.SplineHalfRating):
    """AGMA6123SplineHalfRating

    This is a mastapy class.
    """

    TYPE = _AGMA6123_SPLINE_HALF_RATING

    def __init__(self, instance_to_wrap: 'AGMA6123SplineHalfRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_contact_stress(self) -> 'float':
        """float: 'AllowableContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableContactStress

        if temp is None:
            return None

        return temp

    @property
    def allowable_stress_for_bursting(self) -> 'float':
        """float: 'AllowableStressForBursting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableStressForBursting

        if temp is None:
            return None

        return temp

    @property
    def allowable_stress_for_shearing(self) -> 'float':
        """float: 'AllowableStressForShearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableStressForShearing

        if temp is None:
            return None

        return temp

    @property
    def allowable_torque_for_shearing(self) -> 'float':
        """float: 'AllowableTorqueForShearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableTorqueForShearing

        if temp is None:
            return None

        return temp

    @property
    def allowable_torque_for_wear_and_fretting(self) -> 'float':
        """float: 'AllowableTorqueForWearAndFretting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableTorqueForWearAndFretting

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_ring_bursting(self) -> 'float':
        """float: 'SafetyFactorForRingBursting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForRingBursting

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_shearing(self) -> 'float':
        """float: 'SafetyFactorForShearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForShearing

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_wear_and_fretting(self) -> 'float':
        """float: 'SafetyFactorForWearAndFretting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForWearAndFretting

        if temp is None:
            return None

        return temp
