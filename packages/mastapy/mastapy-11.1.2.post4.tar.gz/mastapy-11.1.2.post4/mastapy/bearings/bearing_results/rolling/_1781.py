"""_1781.py

LoadedNonBarrelRollerBearingDutyCycle
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results import _1722
from mastapy._internal.python_net import python_net_import

_LOADED_NON_BARREL_ROLLER_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedNonBarrelRollerBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonBarrelRollerBearingDutyCycle',)


class LoadedNonBarrelRollerBearingDutyCycle(_1722.LoadedRollingBearingDutyCycle):
    """LoadedNonBarrelRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE = _LOADED_NON_BARREL_ROLLER_BEARING_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'LoadedNonBarrelRollerBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def smt_rib_stress_safety_factor(self) -> 'float':
        """float: 'SMTRibStressSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SMTRibStressSafetyFactor

        if temp is None:
            return None

        return temp
