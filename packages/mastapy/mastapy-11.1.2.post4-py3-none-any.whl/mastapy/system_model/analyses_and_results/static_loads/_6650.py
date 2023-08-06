"""_6650.py

MotorRotorSideFaceDetail
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MOTOR_ROTOR_SIDE_FACE_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MotorRotorSideFaceDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('MotorRotorSideFaceDetail',)


class MotorRotorSideFaceDetail(_0.APIBase):
    """MotorRotorSideFaceDetail

    This is a mastapy class.
    """

    TYPE = _MOTOR_ROTOR_SIDE_FACE_DETAIL

    def __init__(self, instance_to_wrap: 'MotorRotorSideFaceDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_air_gap(self) -> 'float':
        """float: 'AxialAirGap' is the original name of this property."""

        temp = self.wrapped.AxialAirGap

        if temp is None:
            return None

        return temp

    @axial_air_gap.setter
    def axial_air_gap(self, value: 'float'):
        self.wrapped.AxialAirGap = float(value) if value else 0.0

    @property
    def inner_radius(self) -> 'float':
        """float: 'InnerRadius' is the original name of this property."""

        temp = self.wrapped.InnerRadius

        if temp is None:
            return None

        return temp

    @inner_radius.setter
    def inner_radius(self, value: 'float'):
        self.wrapped.InnerRadius = float(value) if value else 0.0

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
    def outer_radius(self) -> 'float':
        """float: 'OuterRadius' is the original name of this property."""

        temp = self.wrapped.OuterRadius

        if temp is None:
            return None

        return temp

    @outer_radius.setter
    def outer_radius(self, value: 'float'):
        self.wrapped.OuterRadius = float(value) if value else 0.0
