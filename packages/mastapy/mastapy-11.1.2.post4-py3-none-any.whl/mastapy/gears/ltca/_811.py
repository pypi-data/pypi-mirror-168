"""_811.py

GearRootFilletStressResults
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.ltca import _804, _805
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_ROOT_FILLET_STRESS_RESULTS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearRootFilletStressResults')


__docformat__ = 'restructuredtext en'
__all__ = ('GearRootFilletStressResults',)


class GearRootFilletStressResults(_0.APIBase):
    """GearRootFilletStressResults

    This is a mastapy class.
    """

    TYPE = _GEAR_ROOT_FILLET_STRESS_RESULTS

    def __init__(self, instance_to_wrap: 'GearRootFilletStressResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_line_index(self) -> 'int':
        """int: 'ContactLineIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLineIndex

        if temp is None:
            return None

        return temp

    @property
    def columns(self) -> 'List[_804.GearFilletNodeStressResultsColumn]':
        """List[GearFilletNodeStressResultsColumn]: 'Columns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Columns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rows(self) -> 'List[_805.GearFilletNodeStressResultsRow]':
        """List[GearFilletNodeStressResultsRow]: 'Rows' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rows

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
