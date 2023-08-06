"""_72.py

LocalNodeInfo
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOCAL_NODE_INFO = python_net_import('SMT.MastaAPI.NodalAnalysis', 'LocalNodeInfo')


__docformat__ = 'restructuredtext en'
__all__ = ('LocalNodeInfo',)


class LocalNodeInfo(_0.APIBase):
    """LocalNodeInfo

    This is a mastapy class.
    """

    TYPE = _LOCAL_NODE_INFO

    def __init__(self, instance_to_wrap: 'LocalNodeInfo.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def first_degrees_of_freedom_index(self) -> 'int':
        """int: 'FirstDegreesOfFreedomIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FirstDegreesOfFreedomIndex

        if temp is None:
            return None

        return temp

    @property
    def number_of_degrees_of_freedom(self) -> 'int':
        """int: 'NumberOfDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfDegreesOfFreedom

        if temp is None:
            return None

        return temp
