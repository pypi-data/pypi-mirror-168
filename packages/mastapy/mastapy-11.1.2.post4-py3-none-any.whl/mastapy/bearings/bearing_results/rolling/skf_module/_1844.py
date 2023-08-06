"""_1844.py

FrictionSources
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FRICTION_SOURCES = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'FrictionSources')


__docformat__ = 'restructuredtext en'
__all__ = ('FrictionSources',)


class FrictionSources(_0.APIBase):
    """FrictionSources

    This is a mastapy class.
    """

    TYPE = _FRICTION_SOURCES

    def __init__(self, instance_to_wrap: 'FrictionSources.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def drag_loss(self) -> 'float':
        """float: 'DragLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DragLoss

        if temp is None:
            return None

        return temp

    @property
    def rolling(self) -> 'float':
        """float: 'Rolling' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rolling

        if temp is None:
            return None

        return temp

    @property
    def seals(self) -> 'float':
        """float: 'Seals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Seals

        if temp is None:
            return None

        return temp

    @property
    def sliding(self) -> 'float':
        """float: 'Sliding' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Sliding

        if temp is None:
            return None

        return temp
