"""_1354.py

ParetoOptimisationInput
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility import _1295
from mastapy.math_utility.measured_ranges import _1372
from mastapy._internal.cast_exception import CastException
from mastapy.math_utility.optimisation import _1364, _1361
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_INPUT = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationInput',)


class ParetoOptimisationInput(_1361.ParetoOptimistaionVariable):
    """ParetoOptimisationInput

    This is a mastapy class.
    """

    TYPE = _PARETO_OPTIMISATION_INPUT

    def __init__(self, instance_to_wrap: 'ParetoOptimisationInput.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_steps(self) -> 'int':
        """int: 'NumberOfSteps' is the original name of this property."""

        temp = self.wrapped.NumberOfSteps

        if temp is None:
            return None

        return temp

    @number_of_steps.setter
    def number_of_steps(self, value: 'int'):
        self.wrapped.NumberOfSteps = int(value) if value else 0

    @property
    def range(self) -> '_1295.Range':
        """Range: 'Range' is the original name of this property."""

        temp = self.wrapped.Range

        if temp is None:
            return None

        if _1295.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @range.setter
    def range(self, value: '_1295.Range'):
        value = value.wrapped if value else None
        self.wrapped.Range = value

    @property
    def specify_input_range_as(self) -> '_1364.SpecifyOptimisationInputAs':
        """SpecifyOptimisationInputAs: 'SpecifyInputRangeAs' is the original name of this property."""

        temp = self.wrapped.SpecifyInputRangeAs

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1364.SpecifyOptimisationInputAs)(value) if value is not None else None

    @specify_input_range_as.setter
    def specify_input_range_as(self, value: '_1364.SpecifyOptimisationInputAs'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpecifyInputRangeAs = value
