"""_1257.py

InterferenceFitRating
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.rating import _1244
from mastapy._internal.python_net import python_net_import

_INTERFERENCE_FIT_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.Rating', 'InterferenceFitRating')


__docformat__ = 'restructuredtext en'
__all__ = ('InterferenceFitRating',)


class InterferenceFitRating(_1244.ShaftHubConnectionRating):
    """InterferenceFitRating

    This is a mastapy class.
    """

    TYPE = _INTERFERENCE_FIT_RATING

    def __init__(self, instance_to_wrap: 'InterferenceFitRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_axial_force_stationary(self) -> 'float':
        """float: 'AllowableAxialForceStationary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableAxialForceStationary

        if temp is None:
            return None

        return temp

    @property
    def allowable_axial_force_at_operating_speed(self) -> 'float':
        """float: 'AllowableAxialForceAtOperatingSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableAxialForceAtOperatingSpeed

        if temp is None:
            return None

        return temp

    @property
    def allowable_torque_stationary(self) -> 'float':
        """float: 'AllowableTorqueStationary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableTorqueStationary

        if temp is None:
            return None

        return temp

    @property
    def allowable_torque_at_operating_speed(self) -> 'float':
        """float: 'AllowableTorqueAtOperatingSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableTorqueAtOperatingSpeed

        if temp is None:
            return None

        return temp

    @property
    def axial_force(self) -> 'float':
        """float: 'AxialForce' is the original name of this property."""

        temp = self.wrapped.AxialForce

        if temp is None:
            return None

        return temp

    @axial_force.setter
    def axial_force(self, value: 'float'):
        self.wrapped.AxialForce = float(value) if value else 0.0

    @property
    def diameter_of_joint(self) -> 'float':
        """float: 'DiameterOfJoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterOfJoint

        if temp is None:
            return None

        return temp

    @property
    def joint_pressure_at_operating_speed(self) -> 'float':
        """float: 'JointPressureAtOperatingSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.JointPressureAtOperatingSpeed

        if temp is None:
            return None

        return temp

    @property
    def length_of_joint(self) -> 'float':
        """float: 'LengthOfJoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfJoint

        if temp is None:
            return None

        return temp

    @property
    def moment(self) -> 'float':
        """float: 'Moment' is the original name of this property."""

        temp = self.wrapped.Moment

        if temp is None:
            return None

        return temp

    @moment.setter
    def moment(self, value: 'float'):
        self.wrapped.Moment = float(value) if value else 0.0

    @property
    def peripheral_speed_of_outer_part(self) -> 'float':
        """float: 'PeripheralSpeedOfOuterPart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeripheralSpeedOfOuterPart

        if temp is None:
            return None

        return temp

    @property
    def peripheral_speed_of_outer_part_causing_loss_of_interference(self) -> 'float':
        """float: 'PeripheralSpeedOfOuterPartCausingLossOfInterference' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeripheralSpeedOfOuterPartCausingLossOfInterference

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_force_stationary(self) -> 'float':
        """float: 'PermissibleAxialForceStationary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialForceStationary

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_force_at_operating_speed(self) -> 'float':
        """float: 'PermissibleAxialForceAtOperatingSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialForceAtOperatingSpeed

        if temp is None:
            return None

        return temp

    @property
    def permissible_torque_stationary(self) -> 'float':
        """float: 'PermissibleTorqueStationary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleTorqueStationary

        if temp is None:
            return None

        return temp

    @property
    def permissible_torque_at_operating_speed(self) -> 'float':
        """float: 'PermissibleTorqueAtOperatingSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleTorqueAtOperatingSpeed

        if temp is None:
            return None

        return temp

    @property
    def radial_force(self) -> 'float':
        """float: 'RadialForce' is the original name of this property."""

        temp = self.wrapped.RadialForce

        if temp is None:
            return None

        return temp

    @radial_force.setter
    def radial_force(self, value: 'float'):
        self.wrapped.RadialForce = float(value) if value else 0.0

    @property
    def required_fit_for_avoidance_of_fretting_wear(self) -> 'float':
        """float: 'RequiredFitForAvoidanceOfFrettingWear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequiredFitForAvoidanceOfFrettingWear

        if temp is None:
            return None

        return temp

    @property
    def rotational_speed(self) -> 'float':
        """float: 'RotationalSpeed' is the original name of this property."""

        temp = self.wrapped.RotationalSpeed

        if temp is None:
            return None

        return temp

    @rotational_speed.setter
    def rotational_speed(self, value: 'float'):
        self.wrapped.RotationalSpeed = float(value) if value else 0.0

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
    def safety_factor_for_axial_force_stationary(self) -> 'float':
        """float: 'SafetyFactorForAxialForceStationary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForAxialForceStationary

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

    @property
    def safety_factor_for_torque_stationary(self) -> 'float':
        """float: 'SafetyFactorForTorqueStationary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForTorqueStationary

        if temp is None:
            return None

        return temp

    @property
    def torque(self) -> 'float':
        """float: 'Torque' is the original name of this property."""

        temp = self.wrapped.Torque

        if temp is None:
            return None

        return temp

    @torque.setter
    def torque(self, value: 'float'):
        self.wrapped.Torque = float(value) if value else 0.0
