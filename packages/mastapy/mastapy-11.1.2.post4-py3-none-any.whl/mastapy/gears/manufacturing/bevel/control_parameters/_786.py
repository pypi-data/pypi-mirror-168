"""_786.py

ConicalManufacturingSMTControlParameters
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel.control_parameters import _783
from mastapy._internal.python_net import python_net_import

_CONICAL_MANUFACTURING_SMT_CONTROL_PARAMETERS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters', 'ConicalManufacturingSMTControlParameters')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalManufacturingSMTControlParameters',)


class ConicalManufacturingSMTControlParameters(_783.ConicalGearManufacturingControlParameters):
    """ConicalManufacturingSMTControlParameters

    This is a mastapy class.
    """

    TYPE = _CONICAL_MANUFACTURING_SMT_CONTROL_PARAMETERS

    def __init__(self, instance_to_wrap: 'ConicalManufacturingSMTControlParameters.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_acceleration(self) -> 'float':
        """float: 'AngularAcceleration' is the original name of this property."""

        temp = self.wrapped.AngularAcceleration

        if temp is None:
            return None

        return temp

    @angular_acceleration.setter
    def angular_acceleration(self, value: 'float'):
        self.wrapped.AngularAcceleration = float(value) if value else 0.0

    @property
    def clearance_between_finish_root_and_rough_root(self) -> 'float':
        """float: 'ClearanceBetweenFinishRootAndRoughRoot' is the original name of this property."""

        temp = self.wrapped.ClearanceBetweenFinishRootAndRoughRoot

        if temp is None:
            return None

        return temp

    @clearance_between_finish_root_and_rough_root.setter
    def clearance_between_finish_root_and_rough_root(self, value: 'float'):
        self.wrapped.ClearanceBetweenFinishRootAndRoughRoot = float(value) if value else 0.0

    @property
    def delta_e(self) -> 'float':
        """float: 'DeltaE' is the original name of this property."""

        temp = self.wrapped.DeltaE

        if temp is None:
            return None

        return temp

    @delta_e.setter
    def delta_e(self, value: 'float'):
        self.wrapped.DeltaE = float(value) if value else 0.0

    @property
    def delta_sigma(self) -> 'float':
        """float: 'DeltaSigma' is the original name of this property."""

        temp = self.wrapped.DeltaSigma

        if temp is None:
            return None

        return temp

    @delta_sigma.setter
    def delta_sigma(self, value: 'float'):
        self.wrapped.DeltaSigma = float(value) if value else 0.0

    @property
    def delta_xp(self) -> 'float':
        """float: 'DeltaXP' is the original name of this property."""

        temp = self.wrapped.DeltaXP

        if temp is None:
            return None

        return temp

    @delta_xp.setter
    def delta_xp(self, value: 'float'):
        self.wrapped.DeltaXP = float(value) if value else 0.0

    @property
    def delta_xw(self) -> 'float':
        """float: 'DeltaXW' is the original name of this property."""

        temp = self.wrapped.DeltaXW

        if temp is None:
            return None

        return temp

    @delta_xw.setter
    def delta_xw(self, value: 'float'):
        self.wrapped.DeltaXW = float(value) if value else 0.0

    @property
    def direction_angle_of_poc(self) -> 'float':
        """float: 'DirectionAngleOfPOC' is the original name of this property."""

        temp = self.wrapped.DirectionAngleOfPOC

        if temp is None:
            return None

        return temp

    @direction_angle_of_poc.setter
    def direction_angle_of_poc(self, value: 'float'):
        self.wrapped.DirectionAngleOfPOC = float(value) if value else 0.0

    @property
    def initial_workhead_offset(self) -> 'float':
        """float: 'InitialWorkheadOffset' is the original name of this property."""

        temp = self.wrapped.InitialWorkheadOffset

        if temp is None:
            return None

        return temp

    @initial_workhead_offset.setter
    def initial_workhead_offset(self, value: 'float'):
        self.wrapped.InitialWorkheadOffset = float(value) if value else 0.0

    @property
    def mean_contact_point_h(self) -> 'float':
        """float: 'MeanContactPointH' is the original name of this property."""

        temp = self.wrapped.MeanContactPointH

        if temp is None:
            return None

        return temp

    @mean_contact_point_h.setter
    def mean_contact_point_h(self, value: 'float'):
        self.wrapped.MeanContactPointH = float(value) if value else 0.0

    @property
    def mean_contact_point_v(self) -> 'float':
        """float: 'MeanContactPointV' is the original name of this property."""

        temp = self.wrapped.MeanContactPointV

        if temp is None:
            return None

        return temp

    @mean_contact_point_v.setter
    def mean_contact_point_v(self, value: 'float'):
        self.wrapped.MeanContactPointV = float(value) if value else 0.0
