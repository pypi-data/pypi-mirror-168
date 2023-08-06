"""_1986.py

MeasuredAndFactorViewModel
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MEASURED_AND_FACTOR_VIEW_MODEL = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'MeasuredAndFactorViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasuredAndFactorViewModel',)


class MeasuredAndFactorViewModel(_0.APIBase):
    """MeasuredAndFactorViewModel

    This is a mastapy class.
    """

    TYPE = _MEASURED_AND_FACTOR_VIEW_MODEL

    def __init__(self, instance_to_wrap: 'MeasuredAndFactorViewModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def normal_module(self) -> 'float':
        """float: 'NormalModule' is the original name of this property."""

        temp = self.wrapped.NormalModule

        if temp is None:
            return None

        return temp

    @normal_module.setter
    def normal_module(self, value: 'float'):
        self.wrapped.NormalModule = float(value) if value else 0.0

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return None

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

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
