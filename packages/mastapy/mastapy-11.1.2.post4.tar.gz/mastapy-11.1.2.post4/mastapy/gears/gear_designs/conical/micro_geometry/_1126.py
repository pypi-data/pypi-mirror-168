"""_1126.py

ConicalGearBiasModification
"""


from mastapy._internal import constructor
from mastapy.gears.micro_geometry import _535
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_BIAS_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry', 'ConicalGearBiasModification')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearBiasModification',)


class ConicalGearBiasModification(_535.BiasModification):
    """ConicalGearBiasModification

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_BIAS_MODIFICATION

    def __init__(self, instance_to_wrap: 'ConicalGearBiasModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def constant_relief(self) -> 'float':
        """float: 'ConstantRelief' is the original name of this property."""

        temp = self.wrapped.ConstantRelief

        if temp is None:
            return None

        return temp

    @constant_relief.setter
    def constant_relief(self, value: 'float'):
        self.wrapped.ConstantRelief = float(value) if value else 0.0
