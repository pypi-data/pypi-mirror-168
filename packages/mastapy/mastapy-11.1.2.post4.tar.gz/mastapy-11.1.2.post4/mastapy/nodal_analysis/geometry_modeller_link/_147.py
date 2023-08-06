"""_147.py

BaseGeometryModellerDimension
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BASE_GEOMETRY_MODELLER_DIMENSION = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'BaseGeometryModellerDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('BaseGeometryModellerDimension',)


class BaseGeometryModellerDimension(_0.APIBase):
    """BaseGeometryModellerDimension

    This is a mastapy class.
    """

    TYPE = _BASE_GEOMETRY_MODELLER_DIMENSION

    def __init__(self, instance_to_wrap: 'BaseGeometryModellerDimension.TYPE'):
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
