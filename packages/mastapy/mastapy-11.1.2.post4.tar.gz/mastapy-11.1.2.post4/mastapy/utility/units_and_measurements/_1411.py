"""_1411.py

Unit
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_UNIT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'Unit')


__docformat__ = 'restructuredtext en'
__all__ = ('Unit',)


class Unit(_0.APIBase):
    """Unit

    This is a mastapy class.
    """

    TYPE = _UNIT

    def __init__(self, instance_to_wrap: 'Unit.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def html_symbol(self) -> 'str':
        """str: 'HTMLSymbol' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HTMLSymbol

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
    def offset(self) -> 'float':
        """float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Offset

        if temp is None:
            return None

        return temp

    @property
    def scale(self) -> 'float':
        """float: 'Scale' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Scale

        if temp is None:
            return None

        return temp

    @property
    def symbol(self) -> 'str':
        """str: 'Symbol' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Symbol

        if temp is None:
            return None

        return temp

    def convert_from_si_unit(self, d: 'float') -> 'float':
        """ 'ConvertFromSIUnit' is the original name of this method.

        Args:
            d (float)

        Returns:
            float
        """

        d = float(d)
        method_result = self.wrapped.ConvertFromSIUnit(d if d else 0.0)
        return method_result

    def convert_to_si_unit(self, d: 'float') -> 'float':
        """ 'ConvertToSIUnit' is the original name of this method.

        Args:
            d (float)

        Returns:
            float
        """

        d = float(d)
        method_result = self.wrapped.ConvertToSIUnit(d if d else 0.0)
        return method_result
