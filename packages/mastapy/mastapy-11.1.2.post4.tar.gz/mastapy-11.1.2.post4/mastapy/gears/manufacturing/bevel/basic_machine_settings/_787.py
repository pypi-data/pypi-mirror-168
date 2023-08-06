"""_787.py

BasicConicalGearMachineSettings
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BASIC_CONICAL_GEAR_MACHINE_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings', 'BasicConicalGearMachineSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BasicConicalGearMachineSettings',)


class BasicConicalGearMachineSettings(_0.APIBase):
    """BasicConicalGearMachineSettings

    This is a mastapy class.
    """

    TYPE = _BASIC_CONICAL_GEAR_MACHINE_SETTINGS

    def __init__(self, instance_to_wrap: 'BasicConicalGearMachineSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def machine_centre_to_back(self) -> 'float':
        """float: 'MachineCentreToBack' is the original name of this property."""

        temp = self.wrapped.MachineCentreToBack

        if temp is None:
            return None

        return temp

    @machine_centre_to_back.setter
    def machine_centre_to_back(self, value: 'float'):
        self.wrapped.MachineCentreToBack = float(value) if value else 0.0

    @property
    def machine_root_angle(self) -> 'float':
        """float: 'MachineRootAngle' is the original name of this property."""

        temp = self.wrapped.MachineRootAngle

        if temp is None:
            return None

        return temp

    @machine_root_angle.setter
    def machine_root_angle(self, value: 'float'):
        self.wrapped.MachineRootAngle = float(value) if value else 0.0

    @property
    def sliding_base(self) -> 'float':
        """float: 'SlidingBase' is the original name of this property."""

        temp = self.wrapped.SlidingBase

        if temp is None:
            return None

        return temp

    @sliding_base.setter
    def sliding_base(self, value: 'float'):
        self.wrapped.SlidingBase = float(value) if value else 0.0

    @property
    def swivel_angle(self) -> 'float':
        """float: 'SwivelAngle' is the original name of this property."""

        temp = self.wrapped.SwivelAngle

        if temp is None:
            return None

        return temp

    @swivel_angle.setter
    def swivel_angle(self, value: 'float'):
        self.wrapped.SwivelAngle = float(value) if value else 0.0

    @property
    def tilt_angle(self) -> 'float':
        """float: 'TiltAngle' is the original name of this property."""

        temp = self.wrapped.TiltAngle

        if temp is None:
            return None

        return temp

    @tilt_angle.setter
    def tilt_angle(self, value: 'float'):
        self.wrapped.TiltAngle = float(value) if value else 0.0
