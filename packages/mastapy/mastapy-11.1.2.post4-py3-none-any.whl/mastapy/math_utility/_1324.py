"""_1324.py

InertiaTensor
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_INERTIA_TENSOR = python_net_import('SMT.MastaAPI.MathUtility', 'InertiaTensor')


__docformat__ = 'restructuredtext en'
__all__ = ('InertiaTensor',)


class InertiaTensor(_0.APIBase):
    """InertiaTensor

    This is a mastapy class.
    """

    TYPE = _INERTIA_TENSOR

    def __init__(self, instance_to_wrap: 'InertiaTensor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def x_axis_inertia(self) -> 'float':
        """float: 'XAxisInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XAxisInertia

        if temp is None:
            return None

        return temp

    @property
    def xy_inertia(self) -> 'float':
        """float: 'XYInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XYInertia

        if temp is None:
            return None

        return temp

    @property
    def xz_inertia(self) -> 'float':
        """float: 'XZInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XZInertia

        if temp is None:
            return None

        return temp

    @property
    def y_axis_inertia(self) -> 'float':
        """float: 'YAxisInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YAxisInertia

        if temp is None:
            return None

        return temp

    @property
    def yz_inertia(self) -> 'float':
        """float: 'YZInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YZInertia

        if temp is None:
            return None

        return temp

    @property
    def z_axis_inertia(self) -> 'float':
        """float: 'ZAxisInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZAxisInertia

        if temp is None:
            return None

        return temp
