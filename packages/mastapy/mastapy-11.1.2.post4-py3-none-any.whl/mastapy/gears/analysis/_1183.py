"""_1183.py

GearSetImplementationDetail
"""


from mastapy._internal import constructor
from mastapy.utility.scripting import _1523
from mastapy.gears.analysis import _1178
from mastapy._internal.python_net import python_net_import

_GEAR_SET_IMPLEMENTATION_DETAIL = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearSetImplementationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetImplementationDetail',)


class GearSetImplementationDetail(_1178.GearSetDesignAnalysis):
    """GearSetImplementationDetail

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_IMPLEMENTATION_DETAIL

    def __init__(self, instance_to_wrap: 'GearSetImplementationDetail.TYPE'):
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
    def user_specified_data(self) -> '_1523.UserSpecifiedData':
        """UserSpecifiedData: 'UserSpecifiedData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UserSpecifiedData

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
