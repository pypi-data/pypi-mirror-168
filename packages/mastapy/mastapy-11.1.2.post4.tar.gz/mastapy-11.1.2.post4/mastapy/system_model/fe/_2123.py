"""_2123.py

DegreeOfFreedomBoundaryConditionLinear
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.fe import _2121
from mastapy._internal.python_net import python_net_import

_DEGREE_OF_FREEDOM_BOUNDARY_CONDITION_LINEAR = python_net_import('SMT.MastaAPI.SystemModel.FE', 'DegreeOfFreedomBoundaryConditionLinear')


__docformat__ = 'restructuredtext en'
__all__ = ('DegreeOfFreedomBoundaryConditionLinear',)


class DegreeOfFreedomBoundaryConditionLinear(_2121.DegreeOfFreedomBoundaryCondition):
    """DegreeOfFreedomBoundaryConditionLinear

    This is a mastapy class.
    """

    TYPE = _DEGREE_OF_FREEDOM_BOUNDARY_CONDITION_LINEAR

    def __init__(self, instance_to_wrap: 'DegreeOfFreedomBoundaryConditionLinear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def displacement(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Displacement' is the original name of this property."""

        temp = self.wrapped.Displacement

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @displacement.setter
    def displacement(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Displacement = value

    @property
    def force(self) -> 'float':
        """float: 'Force' is the original name of this property."""

        temp = self.wrapped.Force

        if temp is None:
            return None

        return temp

    @force.setter
    def force(self, value: 'float'):
        self.wrapped.Force = float(value) if value else 0.0
