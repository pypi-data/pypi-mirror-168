"""_54.py

DiagonalNonlinearStiffness
"""


from mastapy.math_utility import _1341
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DIAGONAL_NONLINEAR_STIFFNESS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'DiagonalNonlinearStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('DiagonalNonlinearStiffness',)


class DiagonalNonlinearStiffness(_0.APIBase):
    """DiagonalNonlinearStiffness

    This is a mastapy class.
    """

    TYPE = _DIAGONAL_NONLINEAR_STIFFNESS

    def __init__(self, instance_to_wrap: 'DiagonalNonlinearStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def theta_x_stiffness(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'ThetaXStiffness' is the original name of this property."""

        temp = self.wrapped.ThetaXStiffness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @theta_x_stiffness.setter
    def theta_x_stiffness(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ThetaXStiffness = value

    @property
    def theta_y_stiffness(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'ThetaYStiffness' is the original name of this property."""

        temp = self.wrapped.ThetaYStiffness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @theta_y_stiffness.setter
    def theta_y_stiffness(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ThetaYStiffness = value

    @property
    def theta_z_stiffness(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'ThetaZStiffness' is the original name of this property."""

        temp = self.wrapped.ThetaZStiffness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @theta_z_stiffness.setter
    def theta_z_stiffness(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ThetaZStiffness = value

    @property
    def x_stiffness(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'XStiffness' is the original name of this property."""

        temp = self.wrapped.XStiffness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @x_stiffness.setter
    def x_stiffness(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.XStiffness = value

    @property
    def y_stiffness(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'YStiffness' is the original name of this property."""

        temp = self.wrapped.YStiffness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @y_stiffness.setter
    def y_stiffness(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.YStiffness = value

    @property
    def z_stiffness(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'ZStiffness' is the original name of this property."""

        temp = self.wrapped.ZStiffness

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @z_stiffness.setter
    def z_stiffness(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ZStiffness = value
