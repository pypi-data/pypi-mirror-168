"""_1728.py

StiffnessRow
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_STIFFNESS_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'StiffnessRow')


__docformat__ = 'restructuredtext en'
__all__ = ('StiffnessRow',)


class StiffnessRow(_0.APIBase):
    """StiffnessRow

    This is a mastapy class.
    """

    TYPE = _STIFFNESS_ROW

    def __init__(self, instance_to_wrap: 'StiffnessRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def comma_separated_values_mn_rad(self) -> 'str':
        """str: 'CommaSeparatedValuesMNRad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CommaSeparatedValuesMNRad

        if temp is None:
            return None

        return temp

    @property
    def row_index(self) -> 'int':
        """int: 'RowIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RowIndex

        if temp is None:
            return None

        return temp
