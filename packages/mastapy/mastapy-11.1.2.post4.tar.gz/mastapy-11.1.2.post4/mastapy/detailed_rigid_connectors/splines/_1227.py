"""_1227.py

StandardSplineHalfDesign
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.splines import _1222
from mastapy._internal.python_net import python_net_import

_STANDARD_SPLINE_HALF_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'StandardSplineHalfDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('StandardSplineHalfDesign',)


class StandardSplineHalfDesign(_1222.SplineHalfDesign):
    """StandardSplineHalfDesign

    This is a mastapy class.
    """

    TYPE = _STANDARD_SPLINE_HALF_DESIGN

    def __init__(self, instance_to_wrap: 'StandardSplineHalfDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def root_fillet_radius_factor(self) -> 'float':
        """float: 'RootFilletRadiusFactor' is the original name of this property."""

        temp = self.wrapped.RootFilletRadiusFactor

        if temp is None:
            return None

        return temp

    @root_fillet_radius_factor.setter
    def root_fillet_radius_factor(self, value: 'float'):
        self.wrapped.RootFilletRadiusFactor = float(value) if value else 0.0
