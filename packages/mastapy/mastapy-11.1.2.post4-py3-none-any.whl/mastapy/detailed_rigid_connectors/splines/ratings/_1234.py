"""_1234.py

DIN5466SplineRating
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.splines.ratings import _1240
from mastapy._internal.python_net import python_net_import

_DIN5466_SPLINE_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings', 'DIN5466SplineRating')


__docformat__ = 'restructuredtext en'
__all__ = ('DIN5466SplineRating',)


class DIN5466SplineRating(_1240.SplineJointRating):
    """DIN5466SplineRating

    This is a mastapy class.
    """

    TYPE = _DIN5466_SPLINE_RATING

    def __init__(self, instance_to_wrap: 'DIN5466SplineRating.TYPE'):
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
    def resultant_shear_force(self) -> 'float':
        """float: 'ResultantShearForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultantShearForce

        if temp is None:
            return None

        return temp
