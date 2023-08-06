"""_1258.py

InterferenceFitDutyCycleRating
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_INTERFERENCE_FIT_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.DutyCycleRatings', 'InterferenceFitDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('InterferenceFitDutyCycleRating',)


class InterferenceFitDutyCycleRating(_0.APIBase):
    """InterferenceFitDutyCycleRating

    This is a mastapy class.
    """

    TYPE = _INTERFERENCE_FIT_DUTY_CYCLE_RATING

    def __init__(self, instance_to_wrap: 'InterferenceFitDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def safety_factor_for_axial_force(self) -> 'float':
        """float: 'SafetyFactorForAxialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForAxialForce

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_torque(self) -> 'float':
        """float: 'SafetyFactorForTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForTorque

        if temp is None:
            return None

        return temp
