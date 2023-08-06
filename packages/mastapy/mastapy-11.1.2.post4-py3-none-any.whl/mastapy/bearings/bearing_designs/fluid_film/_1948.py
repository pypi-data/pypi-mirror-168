"""_1948.py

PlainJournalHousing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1707
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PLAIN_JOURNAL_HOUSING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainJournalHousing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainJournalHousing',)


class PlainJournalHousing(_0.APIBase):
    """PlainJournalHousing

    This is a mastapy class.
    """

    TYPE = _PLAIN_JOURNAL_HOUSING

    def __init__(self, instance_to_wrap: 'PlainJournalHousing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def heat_emitting_area(self) -> 'float':
        """float: 'HeatEmittingArea' is the original name of this property."""

        temp = self.wrapped.HeatEmittingArea

        if temp is None:
            return None

        return temp

    @heat_emitting_area.setter
    def heat_emitting_area(self, value: 'float'):
        self.wrapped.HeatEmittingArea = float(value) if value else 0.0

    @property
    def heat_emitting_area_method(self) -> '_1707.DefaultOrUserInput':
        """DefaultOrUserInput: 'HeatEmittingAreaMethod' is the original name of this property."""

        temp = self.wrapped.HeatEmittingAreaMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1707.DefaultOrUserInput)(value) if value is not None else None

    @heat_emitting_area_method.setter
    def heat_emitting_area_method(self, value: '_1707.DefaultOrUserInput'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HeatEmittingAreaMethod = value
