"""_1974.py

RelativeComponentAlignment
"""


from typing import Generic, TypeVar

from mastapy.math_utility import _1297
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model import _1975
from mastapy import _0
from mastapy.system_model.part_model import _2195
from mastapy._internal.python_net import python_net_import

_RELATIVE_COMPONENT_ALIGNMENT = python_net_import('SMT.MastaAPI.SystemModel', 'RelativeComponentAlignment')


__docformat__ = 'restructuredtext en'
__all__ = ('RelativeComponentAlignment',)


T = TypeVar('T', bound='_2195.Component')


class RelativeComponentAlignment(_0.APIBase, Generic[T]):
    """RelativeComponentAlignment

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _RELATIVE_COMPONENT_ALIGNMENT

    def __init__(self, instance_to_wrap: 'RelativeComponentAlignment.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def alignment_axis(self) -> '_1297.AlignmentAxis':
        """AlignmentAxis: 'AlignmentAxis' is the original name of this property."""

        temp = self.wrapped.AlignmentAxis

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1297.AlignmentAxis)(value) if value is not None else None

    @alignment_axis.setter
    def alignment_axis(self, value: '_1297.AlignmentAxis'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentAxis = value

    @property
    def axial_offset(self) -> '_1975.RelativeOffsetOption':
        """RelativeOffsetOption: 'AxialOffset' is the original name of this property."""

        temp = self.wrapped.AxialOffset

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1975.RelativeOffsetOption)(value) if value is not None else None

    @axial_offset.setter
    def axial_offset(self, value: '_1975.RelativeOffsetOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AxialOffset = value

    @property
    def rotation_angle(self) -> 'float':
        """float: 'RotationAngle' is the original name of this property."""

        temp = self.wrapped.RotationAngle

        if temp is None:
            return None

        return temp

    @rotation_angle.setter
    def rotation_angle(self, value: 'float'):
        self.wrapped.RotationAngle = float(value) if value else 0.0

    @property
    def specified_offset(self) -> 'float':
        """float: 'SpecifiedOffset' is the original name of this property."""

        temp = self.wrapped.SpecifiedOffset

        if temp is None:
            return None

        return temp

    @specified_offset.setter
    def specified_offset(self, value: 'float'):
        self.wrapped.SpecifiedOffset = float(value) if value else 0.0
