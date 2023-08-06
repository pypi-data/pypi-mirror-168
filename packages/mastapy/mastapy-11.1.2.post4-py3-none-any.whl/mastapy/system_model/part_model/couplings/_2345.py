"""_2345.py

RollingRing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _305
from mastapy.system_model.part_model.couplings import _2333
from mastapy._internal.python_net import python_net_import

_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRing',)


class RollingRing(_2333.CouplingHalf):
    """RollingRing

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING

    def __init__(self, instance_to_wrap: 'RollingRing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_diameter(self) -> 'float':
        """float: 'AverageDiameter' is the original name of this property."""

        temp = self.wrapped.AverageDiameter

        if temp is None:
            return None

        return temp

    @average_diameter.setter
    def average_diameter(self, value: 'float'):
        self.wrapped.AverageDiameter = float(value) if value else 0.0

    @property
    def is_internal(self) -> 'bool':
        """bool: 'IsInternal' is the original name of this property."""

        temp = self.wrapped.IsInternal

        if temp is None:
            return None

        return temp

    @is_internal.setter
    def is_internal(self, value: 'bool'):
        self.wrapped.IsInternal = bool(value) if value else False

    @property
    def largest_end(self) -> '_305.Hand':
        """Hand: 'LargestEnd' is the original name of this property."""

        temp = self.wrapped.LargestEnd

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_305.Hand)(value) if value is not None else None

    @largest_end.setter
    def largest_end(self, value: '_305.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LargestEnd = value

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return None

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0
