"""_687.py

MutatableFillet
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters import _685
from mastapy._internal.python_net import python_net_import

_MUTATABLE_FILLET = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'MutatableFillet')


__docformat__ = 'restructuredtext en'
__all__ = ('MutatableFillet',)


class MutatableFillet(_685.MutatableCommon):
    """MutatableFillet

    This is a mastapy class.
    """

    TYPE = _MUTATABLE_FILLET

    def __init__(self, instance_to_wrap: 'MutatableFillet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def radius(self) -> 'float':
        """float: 'Radius' is the original name of this property."""

        temp = self.wrapped.Radius

        if temp is None:
            return None

        return temp

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value else 0.0
