"""_2333.py

CouplingHalf
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2214
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalf',)


class CouplingHalf(_2214.MountableComponent):
    """CouplingHalf

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF

    def __init__(self, instance_to_wrap: 'CouplingHalf.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bore(self) -> 'float':
        """float: 'Bore' is the original name of this property."""

        temp = self.wrapped.Bore

        if temp is None:
            return None

        return temp

    @bore.setter
    def bore(self, value: 'float'):
        self.wrapped.Bore = float(value) if value else 0.0

    @property
    def diameter(self) -> 'float':
        """float: 'Diameter' is the original name of this property."""

        temp = self.wrapped.Diameter

        if temp is None:
            return None

        return temp

    @diameter.setter
    def diameter(self, value: 'float'):
        self.wrapped.Diameter = float(value) if value else 0.0

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
