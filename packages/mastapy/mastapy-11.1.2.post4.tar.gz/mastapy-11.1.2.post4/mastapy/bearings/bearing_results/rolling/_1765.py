"""_1765.py

LoadedCylindricalRollerBearingDutyCycle
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1781
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingDutyCycle',)


class LoadedCylindricalRollerBearingDutyCycle(_1781.LoadedNonBarrelRollerBearingDutyCycle):
    """LoadedCylindricalRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def permissible_continuous_axial_load_safety_factor(self) -> 'float':
        """float: 'PermissibleContinuousAxialLoadSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleContinuousAxialLoadSafetyFactor

        if temp is None:
            return None

        return temp
