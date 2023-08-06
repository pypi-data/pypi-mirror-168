"""_1688.py

ToleranceCombination
"""


from mastapy.bearings.tolerances import _1669
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TOLERANCE_COMBINATION = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'ToleranceCombination')


__docformat__ = 'restructuredtext en'
__all__ = ('ToleranceCombination',)


class ToleranceCombination(_0.APIBase):
    """ToleranceCombination

    This is a mastapy class.
    """

    TYPE = _TOLERANCE_COMBINATION

    def __init__(self, instance_to_wrap: 'ToleranceCombination.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fit(self) -> '_1669.FitType':
        """FitType: 'Fit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Fit

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1669.FitType)(value) if value is not None else None

    @property
    def lower_value(self) -> 'float':
        """float: 'LowerValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LowerValue

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def upper_value(self) -> 'float':
        """float: 'UpperValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UpperValue

        if temp is None:
            return None

        return temp
