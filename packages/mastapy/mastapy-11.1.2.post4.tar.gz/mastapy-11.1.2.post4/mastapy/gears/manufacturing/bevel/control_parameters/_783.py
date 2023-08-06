"""_783.py

ConicalGearManufacturingControlParameters
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MANUFACTURING_CONTROL_PARAMETERS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters', 'ConicalGearManufacturingControlParameters')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearManufacturingControlParameters',)


class ConicalGearManufacturingControlParameters(_0.APIBase):
    """ConicalGearManufacturingControlParameters

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_MANUFACTURING_CONTROL_PARAMETERS

    def __init__(self, instance_to_wrap: 'ConicalGearManufacturingControlParameters.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length_factor_of_contact_pattern(self) -> 'float':
        """float: 'LengthFactorOfContactPattern' is the original name of this property."""

        temp = self.wrapped.LengthFactorOfContactPattern

        if temp is None:
            return None

        return temp

    @length_factor_of_contact_pattern.setter
    def length_factor_of_contact_pattern(self, value: 'float'):
        self.wrapped.LengthFactorOfContactPattern = float(value) if value else 0.0

    @property
    def pinion_root_relief_length(self) -> 'float':
        """float: 'PinionRootReliefLength' is the original name of this property."""

        temp = self.wrapped.PinionRootReliefLength

        if temp is None:
            return None

        return temp

    @pinion_root_relief_length.setter
    def pinion_root_relief_length(self, value: 'float'):
        self.wrapped.PinionRootReliefLength = float(value) if value else 0.0
