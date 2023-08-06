"""_200.py

ShearModulusOrthotropicComponents
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHEAR_MODULUS_ORTHOTROPIC_COMPONENTS = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ShearModulusOrthotropicComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('ShearModulusOrthotropicComponents',)


class ShearModulusOrthotropicComponents(_0.APIBase):
    """ShearModulusOrthotropicComponents

    This is a mastapy class.
    """

    TYPE = _SHEAR_MODULUS_ORTHOTROPIC_COMPONENTS

    def __init__(self, instance_to_wrap: 'ShearModulusOrthotropicComponents.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gxy(self) -> 'float':
        """float: 'GXY' is the original name of this property."""

        temp = self.wrapped.GXY

        if temp is None:
            return None

        return temp

    @gxy.setter
    def gxy(self, value: 'float'):
        self.wrapped.GXY = float(value) if value else 0.0

    @property
    def gxz(self) -> 'float':
        """float: 'GXZ' is the original name of this property."""

        temp = self.wrapped.GXZ

        if temp is None:
            return None

        return temp

    @gxz.setter
    def gxz(self, value: 'float'):
        self.wrapped.GXZ = float(value) if value else 0.0

    @property
    def gyz(self) -> 'float':
        """float: 'GYZ' is the original name of this property."""

        temp = self.wrapped.GYZ

        if temp is None:
            return None

        return temp

    @gyz.setter
    def gyz(self, value: 'float'):
        self.wrapped.GYZ = float(value) if value else 0.0
