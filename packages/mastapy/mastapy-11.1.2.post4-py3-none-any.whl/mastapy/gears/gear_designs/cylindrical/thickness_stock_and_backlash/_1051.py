"""_1051.py

NominalValueSpecification
"""


from typing import Generic, TypeVar

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1044
from mastapy._internal.python_net import python_net_import

_NOMINAL_VALUE_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash', 'NominalValueSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('NominalValueSpecification',)


T = TypeVar('T')


class NominalValueSpecification(_1044.TolerancedValueSpecification['T'], Generic[T]):
    """NominalValueSpecification

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _NOMINAL_VALUE_SPECIFICATION

    def __init__(self, instance_to_wrap: 'NominalValueSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Design' is the original name of this property."""

        temp = self.wrapped.Design

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @design.setter
    def design(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Design = value
