"""_1672.py

InterferenceDetail
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.materials import _245, _223
from mastapy.shafts import _24
from mastapy._internal.cast_exception import CastException
from mastapy.gears.materials import (
    _549, _551, _553, _557,
    _560, _563, _567, _569
)
from mastapy.detailed_rigid_connectors.splines import _1224
from mastapy.cycloidal import _1263, _1269
from mastapy.bolts import _1272, _1276
from mastapy.bearings.tolerances import _1665
from mastapy._internal.python_net import python_net_import

_INTERFERENCE_DETAIL = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'InterferenceDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('InterferenceDetail',)


class InterferenceDetail(_1665.BearingConnectionComponent):
    """InterferenceDetail

    This is a mastapy class.
    """

    TYPE = _INTERFERENCE_DETAIL

    def __init__(self, instance_to_wrap: 'InterferenceDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter_tolerance_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DiameterToleranceFactor' is the original name of this property."""

        temp = self.wrapped.DiameterToleranceFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @diameter_tolerance_factor.setter
    def diameter_tolerance_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DiameterToleranceFactor = value

    @property
    def temperature(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Temperature' is the original name of this property."""

        temp = self.wrapped.Temperature

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @temperature.setter
    def temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Temperature = value

    @property
    def material(self) -> '_245.Material':
        """Material: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        if _245.Material.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material to Material. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
