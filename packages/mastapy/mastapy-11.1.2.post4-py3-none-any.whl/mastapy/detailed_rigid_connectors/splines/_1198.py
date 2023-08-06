"""_1198.py

CustomSplineJointDesign
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.splines import _1223
from mastapy._internal.python_net import python_net_import

_CUSTOM_SPLINE_JOINT_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'CustomSplineJointDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomSplineJointDesign',)


class CustomSplineJointDesign(_1223.SplineJointDesign):
    """CustomSplineJointDesign

    This is a mastapy class.
    """

    TYPE = _CUSTOM_SPLINE_JOINT_DESIGN

    def __init__(self, instance_to_wrap: 'CustomSplineJointDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pressure_angle(self) -> 'float':
        """float: 'PressureAngle' is the original name of this property."""

        temp = self.wrapped.PressureAngle

        if temp is None:
            return None

        return temp

    @pressure_angle.setter
    def pressure_angle(self, value: 'float'):
        self.wrapped.PressureAngle = float(value) if value else 0.0
