"""_572.py

RawMaterial
"""


from mastapy._internal import constructor
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_RAW_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'RawMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('RawMaterial',)


class RawMaterial(_1605.NamedDatabaseItem):
    """RawMaterial

    This is a mastapy class.
    """

    TYPE = _RAW_MATERIAL

    def __init__(self, instance_to_wrap: 'RawMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cost_per_kilogram(self) -> 'float':
        """float: 'CostPerKilogram' is the original name of this property."""

        temp = self.wrapped.CostPerKilogram

        if temp is None:
            return None

        return temp

    @cost_per_kilogram.setter
    def cost_per_kilogram(self, value: 'float'):
        self.wrapped.CostPerKilogram = float(value) if value else 0.0
