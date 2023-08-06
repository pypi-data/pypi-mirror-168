"""_840.py

GearSetLoadCaseBase
"""


from mastapy._internal import constructor
from mastapy.gears.analysis import _1178
from mastapy._internal.python_net import python_net_import

_GEAR_SET_LOAD_CASE_BASE = python_net_import('SMT.MastaAPI.Gears.LoadCase', 'GearSetLoadCaseBase')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetLoadCaseBase',)


class GearSetLoadCaseBase(_1178.GearSetDesignAnalysis):
    """GearSetLoadCaseBase

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_LOAD_CASE_BASE

    def __init__(self, instance_to_wrap: 'GearSetLoadCaseBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def unit_duration(self) -> 'float':
        """float: 'UnitDuration' is the original name of this property."""

        temp = self.wrapped.UnitDuration

        if temp is None:
            return None

        return temp

    @unit_duration.setter
    def unit_duration(self, value: 'float'):
        self.wrapped.UnitDuration = float(value) if value else 0.0
