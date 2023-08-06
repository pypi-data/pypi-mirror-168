"""_35.py

ShaftSectionDamageResults
"""


from mastapy._internal import constructor
from mastapy.shafts import _36
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_SECTION_DAMAGE_RESULTS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSectionDamageResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSectionDamageResults',)


class ShaftSectionDamageResults(_0.APIBase):
    """ShaftSectionDamageResults

    This is a mastapy class.
    """

    TYPE = _SHAFT_SECTION_DAMAGE_RESULTS

    def __init__(self, instance_to_wrap: 'ShaftSectionDamageResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def left_end(self) -> '_36.ShaftSectionEndDamageResults':
        """ShaftSectionEndDamageResults: 'LeftEnd' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftEnd

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_end(self) -> '_36.ShaftSectionEndDamageResults':
        """ShaftSectionEndDamageResults: 'RightEnd' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightEnd

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
