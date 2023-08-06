"""_1173.py

GearImplementationDetail
"""


from mastapy.utility.scripting import _1523
from mastapy._internal import constructor
from mastapy.gears.analysis import _1170
from mastapy._internal.python_net import python_net_import

_GEAR_IMPLEMENTATION_DETAIL = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearImplementationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearImplementationDetail',)


class GearImplementationDetail(_1170.GearDesignAnalysis):
    """GearImplementationDetail

    This is a mastapy class.
    """

    TYPE = _GEAR_IMPLEMENTATION_DETAIL

    def __init__(self, instance_to_wrap: 'GearImplementationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
