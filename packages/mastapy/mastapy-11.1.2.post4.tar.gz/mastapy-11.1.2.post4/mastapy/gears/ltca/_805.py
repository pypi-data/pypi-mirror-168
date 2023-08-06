"""_805.py

GearFilletNodeStressResultsRow
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.ltca import _803
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_FILLET_NODE_STRESS_RESULTS_ROW = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearFilletNodeStressResultsRow')


__docformat__ = 'restructuredtext en'
__all__ = ('GearFilletNodeStressResultsRow',)


class GearFilletNodeStressResultsRow(_0.APIBase):
    """GearFilletNodeStressResultsRow

    This is a mastapy class.
    """

    TYPE = _GEAR_FILLET_NODE_STRESS_RESULTS_ROW

    def __init__(self, instance_to_wrap: 'GearFilletNodeStressResultsRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fillet_row_index(self) -> 'int':
        """int: 'FilletRowIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FilletRowIndex

        if temp is None:
            return None

        return temp

    @property
    def node_results(self) -> 'List[_803.GearFilletNodeStressResults]':
        """List[GearFilletNodeStressResults]: 'NodeResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
